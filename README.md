# Bell's Palsy Facial Symmetry Diagnoser

An open-source, lightweight web application built with Python and Streamlit that evaluates facial symmetry in real-time to detect potential indicators of Bell's Palsy or facial nerve weakness using Google's MediaPipe Face Landmarker.

## ✨ Key Features
* **Dual Input:** Upload photos or use instant webcam capture with automatic horizontal mirror-correction for true left/right orientation.
* **Multi-Zone Feature Tracking:** Maps key facial coordinates and measures distance vectors across the eyebrows, eyes, and mouth relative to a center nose anchor.
* **Vector Visualization:** Draws real-time feature lines and alignment markers on the processed image to visually highlight asymmetry.
* **Ratio Scoring:** Outputs quantitative Healthy vs. Risky asymmetry ratio scores.
* **Recovery Guidance:** Conditionally displays structured dietary recommendations (such as Vitamin B12 and anti-inflammatory foods) and targeted facial physiotherapy exercises if high asymmetry is flagged.

## 🛠️ Tech Stack
* **Framework:** Streamlit
* **Computer Vision:** Google MediaPipe Tasks Vision API, OpenCV, NumPy, Pillow

## 📦 Required Files for Deployment
To deploy this project successfully, ensure these three files are in your GitHub repository root:
1. `app.py` (Main application script)
2. `requirements.txt` (Dependencies)
3. `face_landmarker.task` (Google MediaPipe model asset)

## 🚀 Deployment Steps
1. Create a new public repository on [GitHub](https://github.com/) and name it `bells-palsy-detector`.
2. Upload `app.py`, `requirements.txt`, and `face_landmarker.task` to the repository root and click **Commit changes**.
3. Go to [share.streamlit.io](https://share.streamlit.io/), log in with GitHub, click **New app**, select your repository, and set the main file path to `app.py`.
4. Click **Deploy!**
