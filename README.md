# VidPic Organiser

VidPic Organiser is a computer vision project aimed at organizing images and videos based on detected objects and faces. It utilizes the YOLO object detection model for accurate detection of pretrained objects, with the option to train it on custom faces using the keras implementation of Google's facenet. An SVM classifier is then employed to classify images/videos based on the detections.

## Features
- Accurate object detection using YOLO model
- Option to train on custom faces with facenet
- SVM classifier for image/video classification
- Optimized algorithms for improved performance on CPUs

## Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/Saksham10-11/VidPic-Organizer
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the project:
   ```bash
   python gui.py
   ```

4. Follow the on-screen instructions to use the VidPic Organiser.

## Screenshots
![image](https://github.com/Saksham10-11/VidPic-Organizer/assets/119049709/0cc93e7e-0186-4c17-bfd9-ddde1f4af646)
![image](https://github.com/Saksham10-11/VidPic-Organizer/assets/119049709/63ad57c6-ecce-4e7e-a915-8c21220d0681)

## Contribution
Contributions are welcome! If you'd like to contribute to this project, feel free to fork the repository and submit a pull request.
