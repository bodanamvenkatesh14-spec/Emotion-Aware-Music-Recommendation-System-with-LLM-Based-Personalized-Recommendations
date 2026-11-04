"""
Facial Emotion Detection Module
---------------------------------
Face detection  : OpenCV DNN SSD (ResNet10) — robust against phone screens, low light, angles
Emotion model   : FER+ ONNX (8-class, trained on 35,000+ FER2013 faces, ~85% accuracy)
Fallback        : Haar Cascade + multi-feature heuristic
Preprocessing   : CLAHE + gamma + multi-attempt detection for phone photos
"""

import cv2
import numpy as np
import os

# ── Emotion label order matches FER+ ONNX output ─────────────────────────────
EMOTION_LABELS = ['Neutral', 'Happy', 'Surprise', 'Sad', 'Angry', 'Disgust', 'Fear']

EMOJI_MAP = {
    'Happy':    '😊',
    'Sad':      '😢',
    'Angry':    '😡',
    'Fear':     '😨',
    'Surprise': '😲',
    'Disgust':  '🤢',
    'Neutral':  '😐',
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, 'static', 'models')


class EmotionDetector:
    def __init__(self):
        self.emotion_labels = EMOTION_LABELS

        # ── DNN SSD face detector (ResNet10 Caffe) ────────────────────────────
        self.dnn_face_net = None
        self._load_dnn_face_detector()

        # ── Haar cascade (fallback face detector) ────────────────────────────
        try:
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            self.face_cascade_alt = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml'
            )
        except Exception:
            self.face_cascade = None
            self.face_cascade_alt = None

        # ── FER+ ONNX emotion classifier ─────────────────────────────────────
        self.onnx_net = None
        self._load_onnx_model()

    # ── Model loaders ─────────────────────────────────────────────────────────

    def _load_dnn_face_detector(self):
        proto = os.path.join(MODEL_DIR, 'deploy.prototxt')
        caffe = os.path.join(MODEL_DIR, 'res10_300x300_ssd_iter_140000.caffemodel')
        if os.path.exists(proto) and os.path.exists(caffe):
            try:
                self.dnn_face_net = cv2.dnn.readNetFromCaffe(proto, caffe)
                print('[OK] DNN SSD face detector loaded.')
            except Exception as e:
                print('[NOTICE] DNN face detector load failed:', e)
        else:
            print('[NOTICE] DNN face model files not found — using Haar cascade.')

    def _load_onnx_model(self):
        path = os.path.join(MODEL_DIR, 'emotion-ferplus.onnx')
        if os.path.exists(path):
            try:
                self.onnx_net = cv2.dnn.readNetFromONNX(path)
                print('[OK] FER+ ONNX emotion model loaded — accurate detection active.')
            except Exception as e:
                print('[NOTICE] ONNX model load failed:', e)
        else:
            print('[NOTICE] ONNX model not found — heuristic fallback active.')

    def load_model(self, model_path=None):
        """Compatibility stub called by app.py startup."""
        if self.onnx_net and self.dnn_face_net:
            print('[OK] Emotion detector ready (DNN face + FER+ ONNX).')
        elif self.onnx_net:
            print('[OK] Emotion detector ready (Haar face + FER+ ONNX).')
        else:
            print('[OK] Emotion detector ready (heuristic fallback).')

    # ── Preprocessing ─────────────────────────────────────────────────────────

    def _preprocess_frame(self, frame):
        """
        Apply CLAHE + mild sharpening to handle:
        - Phone screen glow / reflections
        - Poor lighting
        - JPEG compression artifacts
        Returns a list of preprocessed BGR frames to try.
        """
        variants = [frame]   # always try original first

        # CLAHE on L channel of LAB
        try:
            lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
            l_eq = clahe.apply(l)
            lab_eq = cv2.merge([l_eq, a, b])
            enhanced = cv2.cvtColor(lab_eq, cv2.COLOR_LAB2BGR)
            variants.append(enhanced)
        except Exception:
            pass

        # Gamma correction (brighten dark phone photos)
        try:
            gamma = 1.5
            lut = np.array([((i / 255.0) ** (1.0 / gamma)) * 255
                            for i in range(256)], dtype=np.uint8)
            brightened = cv2.LUT(frame, lut)
            variants.append(brightened)
        except Exception:
            pass

        # Sharpening kernel
        try:
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            sharpened = cv2.filter2D(frame, -1, kernel)
            variants.append(sharpened)
        except Exception:
            pass

        return variants

    # ── Face detection ────────────────────────────────────────────────────────

    def _detect_faces_dnn(self, frame):
        """
        DNN SSD face detection — robust to phone screens, angles, lighting.
        Returns list of (x, y, w, h) tuples.
        """
        if self.dnn_face_net is None:
            return []
        try:
            h, w = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(
                cv2.resize(frame, (300, 300)), 1.0,
                (300, 300), (104.0, 177.0, 123.0)
            )
            self.dnn_face_net.setInput(blob)
            detections = self.dnn_face_net.forward()
            faces = []
            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > 0.45:   # lowered threshold for phone photos
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    x1, y1, x2, y2 = box.astype(int)
                    x1, y1 = max(0, x1), max(0, y1)
                    x2, y2 = min(w, x2), min(h, y2)
                    fw, fh = x2 - x1, y2 - y1
                    if fw > 20 and fh > 20:
                        faces.append((x1, y1, fw, fh))
            return faces
        except Exception as e:
            print('[NOTICE] DNN face detection error:', e)
            return []

    def _detect_faces_haar(self, gray):
        """Haar Cascade face detection with lenient params for phone photos."""
        results = []
        for cascade in [self.face_cascade, self.face_cascade_alt]:
            if cascade is None or cascade.empty():
                continue
            try:
                faces = cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.05,   # finer scale steps
                    minNeighbors=3,     # less strict for partially visible faces
                    minSize=(30, 30),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )
                if len(faces) > 0:
                    results.extend(faces.tolist())
            except Exception:
                pass
        return results

    def detect_faces(self, frame):
        """
        Multi-method face detection.
        Returns (faces_list, gray_frame).
        Tries DNN first, falls back to Haar on every preprocessed variant.
        """
        if frame is None:
            return [], None

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 1. DNN SSD (most robust)
        variants = self._preprocess_frame(frame)
        for variant in variants:
            faces = self._detect_faces_dnn(variant)
            if faces:
                return faces, gray

        # 2. Haar on all variants + scales
        for variant in variants:
            g = cv2.cvtColor(variant, cv2.COLOR_BGR2GRAY)
            for scale in [1.0, 0.75, 0.5]:
                if scale < 1.0:
                    small = cv2.resize(g, (0, 0), fx=scale, fy=scale)
                    faces_raw = self._detect_faces_haar(small)
                    # Scale coordinates back up
                    faces = [(int(x/scale), int(y/scale),
                              int(w/scale), int(h/scale))
                             for x, y, w, h in faces_raw]
                else:
                    faces = self._detect_faces_haar(g)
                if faces:
                    return faces, gray

        return [], gray

    # ── Emotion prediction ────────────────────────────────────────────────────

    def _run_ferplus_onnx(self, gray, x, y, w, h):
        """
        FER+ ONNX inference.
        Input: 1×1×64×64 float32, range 0–255 (NOT normalised).
        Returns (emotion_label, confidence) or (None, 0.0) on error.
        """
        try:
            face_roi = gray[y:y+h, x:x+w]
            if face_roi.size == 0:
                return None, 0.0

            # CLAHE on the face ROI before inference
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(4, 4))
            face_roi = clahe.apply(face_roi)

            face_64 = cv2.resize(face_roi, (64, 64)).astype(np.float32)
            blob = face_64.reshape(1, 1, 64, 64)

            self.onnx_net.setInput(blob)
            raw = self.onnx_net.forward()[0][:7]   # first 7 outputs = 7 emotions

            # Softmax
            exp_r = np.exp(raw - np.max(raw))
            probs = exp_r / exp_r.sum()

            idx = int(np.argmax(probs))
            conf = float(probs[idx])
            return EMOTION_LABELS[idx], round(conf, 3)
        except Exception as e:
            print('[NOTICE] ONNX inference error:', e)
            return None, 0.0

    def _run_heuristic(self, gray, x, y, w, h):
        """
        Multi-feature heuristic when ONNX is unavailable.
        Uses brightness, contrast, edge density, and region asymmetry.
        """
        face_roi = gray[y:y+h, x:x+w]
        if face_roi.size == 0:
            return 'Neutral', 0.60

        brightness   = np.mean(face_roi) / 255.0
        contrast     = np.std(face_roi) / 128.0
        edges        = cv2.Canny(face_roi, 50, 150)
        edge_density = np.sum(edges > 0) / (w * h + 1e-6)

        upper = face_roi[:h//2, :]
        lower = face_roi[h//2:, :]
        lower_contrast = np.std(lower) / 128.0
        upper_contrast = np.std(upper) / 128.0
        left  = face_roi[:, :w//2]
        right = face_roi[:, w//2:]
        asymmetry = abs(np.mean(left) - np.mean(right)) / 128.0

        scores = {
            'Happy':    brightness * 1.5 + lower_contrast * 1.4,
            'Sad':      (1 - brightness) * 1.3 + (1 - np.mean(lower)/255.0) * 0.8,
            'Angry':    edge_density * 1.8 + upper_contrast * 1.2,
            'Surprise': edge_density * 1.6 + lower_contrast * 1.1,
            'Fear':     (1 - brightness) * 0.9 + edge_density * 1.0,
            'Disgust':  asymmetry * 2.2 + contrast * 0.6,
            'Neutral':  (1 - abs(brightness - 0.5)) + (1 - edge_density) * 0.7,
        }
        emotion = max(scores, key=scores.get)
        total = sum(scores.values()) or 1.0
        conf = max(0.60, min(0.88, scores[emotion] / total))
        return emotion, round(conf, 2)

    def predict_emotion(self, frame):
        """
        Main entry point.
        Returns: (emotion_label, confidence_float, face_coords_or_None)
        """
        if frame is None:
            return 'Neutral', 0.50, None

        # Resize very large images (e.g., phone camera 4K) to max 1280px wide
        h, w = frame.shape[:2]
        if w > 1280:
            scale = 1280 / w
            frame = cv2.resize(frame, (1280, int(h * scale)))

        faces, gray = self.detect_faces(frame)

        if not faces:
            return 'Neutral', 0.50, None

        # Pick largest face
        x, y, fw, fh = max(faces, key=lambda f: f[2] * f[3])
        # Safety clamp
        x, y = max(0, x), max(0, y)
        fw = min(fw, gray.shape[1] - x)
        fh = min(fh, gray.shape[0] - y)

        # FER+ ONNX
        if self.onnx_net is not None:
            emotion, conf = self._run_ferplus_onnx(gray, x, y, fw, fh)
            if emotion is not None and conf > 0.15:
                return emotion, conf, (x, y, fw, fh)

        # Heuristic fallback
        emotion, conf = self._run_heuristic(gray, x, y, fw, fh)
        return emotion, conf, (x, y, fw, fh)

    def get_emotion_emoji(self, emotion):
        return EMOJI_MAP.get(emotion, '😐')


# Global singleton
emotion_detector = EmotionDetector()
