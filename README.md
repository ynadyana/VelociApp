# VelociApp — Desktop Real-Time Road Damage Detection (YOLOv11L)

VelociApp is a **desktop application** for real-time road damage detection using **YOLOv11L** object detection. It processes **live camera/video input** and displays detections with **bounding boxes and confidence scores**, enabling faster and more consistent visual inspection of road conditions.

## Key Features
- Desktop-based interface for **real-time detection**
- Supports **video input / live feed** with on-screen results
- Displays **bounding boxes + confidence score** for each detection
- Detects **7 road damage categories**:
  1. Longitudinal cracks  
  2. Transverse cracks  
  3. Alligator cracks  
  4. Potholes  
  5. White line blur  
  6. Faded pedestrian crossing  
  7. Manhole  

## Model Selection
Multiple YOLO model sizes were evaluated. Smaller variants were tested but did not meet the project’s real-time requirements (e.g., reduced detection consistency in real road scenes). **YOLOv11L** was selected for more stable and reliable detection performance.

## Performance & Hardware
- **Recommended:** NVIDIA GPU (CUDA) for smooth real-time inference
- **CPU Mode:** Supported, but not suitable for real-time usage due to lower FPS and slower responsiveness

## Packaging & Deployment
The application is packaged for Windows distribution using:
- **PyInstaller** (to bundle the Python application)
- **Inno Setup** (to generate an installation package)

## Project Structure
- `src/` — application source code  
- `src/assets/` — UI assets/resources  
- `src/models/` — model weights location  
- `screenshots/` — sample detections and UI previews  

## Demo
Add your screenshots to `/screenshots` and embed them here:
![VelociApp Real-Time Detection](screenshots/demo.png)

## Notes
Model weights may be excluded from the repository due to file size. If required, place the weights under `src/models/` (e.g., `best_yolov11-L.pt`) before running the application.
