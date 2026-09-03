Bell's Palsy Facial Symmetry Diagnostic Tool
An open-source, lightweight web application built with Python and Streamlit that evaluates facial symmetry in real-time to detect potential indicators of Bell's Palsy or facial nerve weakness. The app uses Google's MediaPipe Face Landmarker to extract geometric coordinates without requiring heavy machine learning models or API keys.

✨ Key Features
Dual Input Modes: Supports both instant webcam capture (with automatic horizontal mirror-correction for true left/right orientation) and direct photo uploads (PNG, JPG, JPEG).

Multi-Zone Feature Tracking: Maps key facial coordinates across the eyebrows, eyes, and mouth corners relative to a center nose anchor.

Vector Visualization: Draws real-time feature lines and alignment markers on the processed image to visually highlight asymmetry.

Quantitative Asymmetry Ratios: Calculates Euclidean distances between left and right facial features to output a distinct Healthy vs. Risky ratio score.

Actionable Recovery Guidance: Conditionally renders structured dietary recommendations (such as Vitamin B12 and anti-inflammatory foods) and targeted facial physiotherapy exercises if high asymmetry is flagged.

🛠️ Tech Stack
Frontend & Web Framework: Streamlit

Facial Landmark Detection: Google MediaPipe Tasks Vision API

Image Processing & Geometry: OpenCV (cv2), NumPy, Pillow (PIL)

🚀 Running Locally
To run this project on your local machine, follow these steps:

Clone the repository:

Bash
git clone https://github.com/your-username/bells-palsy-detector.git
cd bells-palsy-detector
Install the dependencies:

Bash
pip install -r requirements.txt
Download the model file:
Ensure the face_landmarker.task file is placed in the root directory of your project folder. (You can download it directly from the Google MediaPipe Model Storage).

Run the Streamlit app:

Bash
streamlit run app.py
📦 Deployment on Streamlit Community Cloud
This project is optimized for instant deployment via Streamlit Cloud:

Push app.py, requirements.txt, and face_landmarker.task to your public GitHub repository.

Log in to Streamlit Community Cloud.

Click New app, select your repository, specify app.py as the main file path, and click Deploy.
