import cv2
import numpy as np
import os


HAAR_FRONTAL = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
HAAR_PROFILE  = cv2.data.haarcascades + 'haarcascade_profileface.xml'
HAAR_EYE      = cv2.data.haarcascades + 'haarcascade_eye.xml'


def verify_face_with_opencv(image_file):
    """
    Verifies that an uploaded image contains exactly one clear human face.

    Steps
    -----
    1. Read image bytes into OpenCV
    2. Convert to grayscale
    3. Detect faces using Haar Cascade
    4. Validate: exactly 1 face, minimum size, eyes detected inside face region

    Returns
    -------
    dict  {verified: bool, reason: str, confidence: float, face_count: int}
    """

    # ── 1. Read image ──────────────────────────────────────
    try:
        img_bytes = image_file.read()
        if len(img_bytes) < 5000:
            return {
                'verified': False,
                'reason': 'Image file is too small. Please upload a clear selfie.',
                'face_count': 0,
            }

        nparr = np.frombuffer(img_bytes, np.uint8)
        img   = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return {
                'verified': False,
                'reason': 'Could not read the image. Please upload a JPEG or PNG file.',
                'face_count': 0,
            }
    except Exception as e:
        return {
            'verified': False,
            'reason': f'Image processing error: {str(e)}',
            'face_count': 0,
        }

    # ── 2. Validate image dimensions ───────────────────────
    h, w = img.shape[:2]
    if w < 100 or h < 100:
        return {
            'verified': False,
            'reason': 'Image resolution too low. Please upload a photo at least 200x200 pixels.',
            'face_count': 0,
        }

    # ── 3. Convert to grayscale ────────────────────────────
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)  # improve contrast

    # ── 4. Load Haar cascades ──────────────────────────────
    if not os.path.exists(HAAR_FRONTAL):
        return {
            'verified': False,
            'reason': 'OpenCV cascade files not found. Please reinstall opencv-python.',
            'face_count': 0,
        }

    face_cascade = cv2.CascadeClassifier(HAAR_FRONTAL)
    eye_cascade  = cv2.CascadeClassifier(HAAR_EYE)

    # ── 5. Detect faces ────────────────────────────────────
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(80, 80),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )

    face_count = len(faces)

    if face_count == 0:
        # Try with less strict parameters
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=3,
            minSize=(60, 60),
        )
        face_count = len(faces)

    if face_count == 0:
        return {
            'verified': False,
            'reason': 'No face detected. Please upload a clear front-facing selfie with good lighting.',
            'face_count': 0,
        }

    if face_count > 1:
        return {
            'verified': False,
            'reason': f'{face_count} faces detected. Please upload a selfie with only your face visible.',
            'face_count': face_count,
        }

    # ── 6. Validate face size ──────────────────────────────
    fx, fy, fw, fh = faces[0]
    face_area  = fw * fh
    image_area = w * h
    face_ratio = face_area / image_area

    if face_ratio < 0.03:
        return {
            'verified': False,
            'reason': 'Face is too small in the image. Please move closer to the camera.',
            'face_count': 1,
        }

    # ── 7. Detect eyes inside face region ─────────────────
    face_roi_gray = gray[fy:fy+fh, fx:fx+fw]
    eyes = eye_cascade.detectMultiScale(
        face_roi_gray,
        scaleFactor=1.1,
        minNeighbors=3,
        minSize=(20, 20),
    )

    eye_count = len(eyes)

    # ── 8. Calculate confidence score ─────────────────────
    confidence = 70.0

    if eye_count >= 2:
        confidence += 20.0  # Both eyes visible

    if face_ratio > 0.1:
        confidence += 10.0  # Face is large enough

    confidence = min(confidence, 99.0)

    # We allow single eye detection (profile photo, glasses, etc.)
    # but require at least one eye for stricter verification
    if eye_count == 0:
        return {
            'verified': False,
            'reason': 'Eyes not detected. Please ensure your face is clearly visible and remove sunglasses.',
            'face_count': 1,
            'confidence': 40.0,
        }

    return {
        'verified': True,
        'reason': 'Face verified successfully.',
        'face_count': 1,
        'eye_count': eye_count,
        'confidence': confidence,
        'face_size_ratio': round(face_ratio * 100, 1),
    }