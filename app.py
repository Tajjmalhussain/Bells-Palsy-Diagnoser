%%writefile app.py
import streamlit as st
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
from PIL import Image

st.set_page_config(page_title="Bells Palsy Diagnoser", page_icon="⚕️")
st.title("⚕️ Bell's Palsy Diagnostic Tool")
st.write("Take a picture with your webcam or upload a photo to analyze facial symmetry, eyebrows, eyes, and mouth features.")

base_options = python.BaseOptions(model_asset_path='face_landmarker.task')
options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    output_face_blendshapes=False,
    output_facial_transformation_matrixes=False,
    num_faces=1
)
detector = vision.FaceLandmarker.create_from_options(options)

def calculate_distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def analyze_and_draw_face(image, is_webcam=False):
    img_array = np.array(image.convert('RGB'))
    if is_webcam:
        img_array = cv2.flip(img_array, 1)
        
    h_orig, w_orig, _ = img_array.shape
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_array)
    detection_result = detector.detect(mp_image)
    
    if not detection_result.face_landmarks:
        return None, None, "No face detected. Please ensure your face is well-lit and front-facing."
        
    landmarks = detection_result.face_landmarks[0]
    
    def get_coords(idx):
        return (int(landmarks[idx].x * w_orig), int(landmarks[idx].y * h_orig))
        
    nose = get_coords(1)
    mouth_left, mouth_right = get_coords(291), get_coords(61)
    eye_left_top, eye_left_bottom = get_coords(386), get_coords(374)
    eye_right_top, eye_right_bottom = get_coords(159), get_coords(145)
    brow_left = get_coords(70)
    brow_right = get_coords(300)
    
    annotated_image = img_array.copy()
    cv2.circle(annotated_image, nose, 6, (0, 255, 255), -1) 
    cv2.line(annotated_image, nose, mouth_left, (255, 0, 0), 2)
    cv2.line(annotated_image, nose, mouth_right, (0, 255, 0), 2)
    cv2.line(annotated_image, nose, brow_left, (255, 0, 0), 2)
    cv2.line(annotated_image, nose, brow_right, (0, 255, 0), 2)
    
    for pt in [mouth_left, mouth_right, brow_left, brow_right]:
        cv2.circle(annotated_image, pt, 5, (255, 255, 255), -1)
    
    dist_mouth_l = calculate_distance(nose, mouth_left)
    dist_mouth_r = calculate_distance(nose, mouth_right)
    dist_eye_l = calculate_distance(eye_left_top, eye_left_bottom)
    dist_eye_r = calculate_distance(eye_right_top, eye_right_bottom)
    dist_brow_l = calculate_distance(nose, brow_left)
    dist_brow_r = calculate_distance(nose, brow_right)
    
    mouth_asymmetry = abs(dist_mouth_l - dist_mouth_r) / max(dist_mouth_l, dist_mouth_r) * 100
    eye_asymmetry = abs(dist_eye_l - dist_eye_r) / max(dist_eye_l, dist_eye_r) * 100
    brow_asymmetry = abs(dist_brow_l - dist_brow_r) / max(dist_brow_l, dist_brow_r) * 100
    
    total_asymmetry = (mouth_asymmetry + eye_asymmetry + brow_asymmetry) / 3
    risky_ratio = min(100.0, total_asymmetry * 3)
    healthy_ratio = max(0.0, 100.0 - risky_ratio)
    
    metrics = {
        "healthy_ratio": round(healthy_ratio, 1),
        "risky_ratio": round(risky_ratio, 1),
        "mouth_left_dist": round(dist_mouth_l, 1),
        "mouth_right_dist": round(dist_mouth_r, 1),
        "eye_left_dist": round(dist_eye_l, 1),
        "eye_right_dist": round(dist_eye_r, 1),
        "brow_left_dist": round(dist_brow_l, 1),
        "brow_right_dist": round(dist_brow_r, 1)
    }
    
    return annotated_image, metrics, None

input_mode = st.radio("Choose Input Method:", ("Instant Capture (Webcam)", "Upload Photo"))

img_file = None
is_webcam_mode = False

if input_mode == "Instant Capture (Webcam)":
    img_file = st.camera_input("Take a direct picture using your camera")
    is_webcam_mode = True
else:
    img_file = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg'])
    is_webcam_mode = False

if img_file is not None:
    image = Image.open(img_file)
    
    with st.spinner("Analyzing facial structure, eyebrows, and symmetry..."):
        annotated_img, metrics, error = analyze_and_draw_face(image, is_webcam=is_webcam_mode)
        
    if error:
        st.error(error)
    else:
        st.image(annotated_img, caption="Analyzed Face (Blue: Left Feature, Green: Right Feature, Cyan: Center Anchor)", use_container_width=True)
        
        st.subheader("Diagnostic Ratios")
        col1, col2 = st.columns(2)
        col1.metric("Healthy Symmetry", f"{metrics['healthy_ratio']}%")
        col2.metric("Risky / Asymmetry", f"{metrics['risky_ratio']}%")
        
        with st.expander("📊 Detailed Left vs Right Feature Vector Metrics"):
            st.write(f"* **Left Eyebrow-to-Nose Distance:** {metrics['brow_left_dist']} px")
            st.write(f"* **Right Eyebrow-to-Nose Distance:** {metrics['brow_right_dist']} px")
            st.write(f"* **Left Eye Opening Span:** {metrics['eye_left_dist']} px")
            st.write(f"* **Right Eye Opening Span:** {metrics['eye_right_dist']} px")
            st.write(f"* **Left Mouth-to-Nose Distance:** {metrics['mouth_left_dist']} px")
            st.write(f"* **Right Mouth-to-Nose Distance:** {metrics['mouth_right_dist']} px")
        
        if metrics['risky_ratio'] > 25.0:
            st.warning("⚠️ High facial asymmetry detected. This may indicate a risk of Bell's Palsy or facial nerve weakness.")
            
            st.write("---")
            st.write("### 🥗 Recommended Food Plan for Nerve Recovery")
            st.write("* **Vitamin B12:** Eggs, fortified cereals, and salmon to help repair nerve damage.")
            st.write("* **Anti-inflammatory Foods:** Leafy greens, berries, and healthy fats.")
            
            st.write("### 🏋️‍♂️ Recommended Facial Exercise Plan")
            st.write("* **Eyebrow Lifts:** Gently raise and lower eyebrows using your fingers to assist if one side lags.")
            st.write("* **Gentle Eye Closures:** Squeeze eyes shut softly and hold for 5 seconds.")
            st.write("* **Symmetrical Smiling:** Practice gentle closed-mouth smiles in front of a mirror.")
        else:
            st.success("✅ Your face appears balanced, symmetrical, and healthy!")