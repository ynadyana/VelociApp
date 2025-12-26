import os
import torch
import requests
import sys
sys.setrecursionlimit(10000)
import cv2
import csv
from fpdf import FPDF
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QFileDialog, QDialog, QFormLayout, QLineEdit, QProgressBar, QSizePolicy, QMessageBox, QSpacerItem
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtCore import QTimer, Qt, QSize
from ultralytics import YOLO
import time

sys.setrecursionlimit(10000)

#https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Define the custom button class here
class CustomButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #36454F;
                color: white;
                padding: 10px;
                font-size: 16px;
                border-radius: 10px;
                width: 200px;
                transition: background-color 0.3s ease;
            }

            QPushButton:hover {
                background-color: #36454F;
            }

            QPushButton:pressed {
                background-color: #36454F;
            }
        """)
        # Adding hover and pressed effect within PyQt5's event loop
        self.setAutoFillBackground(True)

    def enterEvent(self, event):
        """Override the enterEvent to simulate hover effect"""
        self.setStyleSheet("""
            QPushButton {
                background-color: #868686;
                color: white;
                padding: 10px;
                font-size: 16px;
                border-radius: 10px;
                width: 200px;
            }

            QPushButton:pressed {
                background-color: #868686;
            }
        """)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Override the leaveEvent to reset hover effect"""
        self.setStyleSheet("""
            QPushButton {
                background-color: #36454F;
                color: white;
                padding: 10px;
                font-size: 16px;
                border-radius: 10px;
                width: 200px;
            }

            QPushButton:pressed {
                background-color: #36454F;
            }
        """)
        super().leaveEvent(event)

class CustomButton1(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #36454F;
                color: white;
                padding: 30px;
                font-size: 18px;
                border-radius: 15px;
                width: 250px;
                height: 50px;
                transition: background-color 0.3s ease;
            }

            QPushButton:hover {
                background-color: #36454F;
            }

            QPushButton:pressed {
                background-color: #36454F;
            }
        """)
        # Adding hover and pressed effect within PyQt5's event loop
        self.setAutoFillBackground(True)

    def enterEvent(self, event):
        """Override the enterEvent to simulate hover effect"""
        self.setStyleSheet("""
            QPushButton {
                background-color: #868686;
                color: white;
                padding: 30px;
                font-size: 18px;
                border-radius: 15px;
                width: 250px;
            }

            QPushButton:pressed {
                background-color: #868686;
            }
        """)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Override the leaveEvent to reset hover effect"""
        self.setStyleSheet("""
            QPushButton {
                background-color: #2c2f35;
                color: white;
                padding: 10px;
                font-size: 16px;
                border-radius: 10px;
                width: 200px;
                height: 50px;
            }

            QPushButton:pressed {
                background-color: #2c2f35;
            }
        """)
        super().leaveEvent(event)

class CustomButton3(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #36454F;
                color: white;
                padding: 12px 20px;
                font-size: 16px;
                border-radius: 10px;
                transition: background-color 0.3s ease;
            }

            QPushButton:pressed {
                background-color: #36454F;
            }
        """)
        self.setAutoFillBackground(True)

    def enterEvent(self, event):
        """Override the enterEvent to simulate hover effect"""
        self.setStyleSheet("""
            QPushButton {
                background-color: #868686;
                color: white;
                padding: 12px 20px;
                font-size: 16px;
                border-radius: 10px;
            }

            QPushButton:pressed {
                background-color: #868686;
            }
        """)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Override the leaveEvent to reset hover effect"""
        self.setStyleSheet("""
            QPushButton {
                background-color: #2c2f35;
                color: white;
                padding: 12px 20px;
                font-size: 16px;
                border-radius: 10px;
            }

            QPushButton:pressed {
                background-color: #2c2f35;
            }
        """)
        super().leaveEvent(event)



class YOLOApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Veloci")

        # Set background color for QWidget and all layouts
        self.setStyleSheet("background-color:#2c2f35;")  # Dark green background color for the main window

        self.setWindowIcon(QIcon(resource_path("assets/logo.png")))

        # Logo setup
        self.logo_label = QLabel(self)
        self.logo_image = QPixmap(resource_path("assets/logo.png"))  # Path to your logo file
        self.logo_image = self.logo_image.scaled(200, 200, Qt.KeepAspectRatio)  # Adjust size to fit properly
        self.logo_label.setPixmap(self.logo_image)
        self.logo_label.setAlignment(Qt.AlignCenter)

        # Title setup
        self.title_label = QLabel("VELOCI: Road Damage Detection System", self)
        self.title_label.setStyleSheet("font-size: 30px; color: white; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignCenter)

        # Start Button setup
        self.start_button = CustomButton("Start", self)
        self.start_button.setStyleSheet("background-color: #36454F; color: white; padding: 10px; font-size: 16px; border-radius: 10px; width: 200px;")
        self.start_button.clicked.connect(self.show_detection_type_page)

        # Layout setup for the homepage
        layout = QVBoxLayout()
        layout.addWidget(self.logo_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.start_button)
        layout.setContentsMargins(50, 50, 50, 50)  # Add margins to the layout for better spacing
        layout.setSpacing(20)  # Adjust spacing between widgets
        layout.setAlignment(Qt.AlignCenter)  # Center the content
        self.setLayout(layout)

        # Make the window full screen
        self.showFullScreen()  # Open in full-screen mode

    def keyPressEvent(self, event):
        """Override the keyPressEvent to listen for the Esc key."""
        if event.key() == Qt.Key_Escape:
            self.close()  # Close the window when Esc is pressed
        elif event.key() == Qt.Key_M:  # You can also add functionality to minimize
            self.showMinimized()  # Minimize the window when M is pressed

    def show_detection_type_page(self):
        # Hide the homepage and show the detection type page
        self.hide()
        self.detection_type_page = DetectionTypePage()
        self.detection_type_page.show()


class DetectionTypePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Detection Type")

        # Set background color for the detection type page
        self.setStyleSheet("background-color: #2c2f35;")  # Dark green background color

        # Create the layout for the two boxes (submit video and real-time detection)
        main_layout = QHBoxLayout(self)

        # Left side: Submit Video Recording
        self.submit_video_box = QFrame(self)
        self.submit_video_box.setStyleSheet(""" 
            background-color: #36454F;
            border-radius: 10px;
            padding: 20px;
            margin-right: 20px;
        """)
        self.submit_video_box.setFixedWidth(900)  # Adjust the width of the video submission box
        self.submit_video_box.setFixedHeight(700)  # Adjust the height of the video submission box
        left_layout = QVBoxLayout(self.submit_video_box)
        self.submit_video_label = QLabel("Submit Video Recording", self.submit_video_box)
        self.submit_video_label.setStyleSheet("font-size: 22px; color: white; font-weight: bold;")
        self.submit_video_label.setAlignment(Qt.AlignCenter)
        self.upload_button = CustomButton1("Upload", self.submit_video_box)
        self.upload_button.setStyleSheet("background-color: #2c2f35; color: white; padding: 30px; font-size: 18px; border-radius: 15px; width: 250px;")
        self.upload_button.clicked.connect(self.show_upload_form)
        left_layout.addWidget(self.submit_video_label)
        left_layout.addWidget(self.upload_button)
        left_layout.setAlignment(Qt.AlignCenter)

        # Right side: Real-time Detection
        self.real_time_box = QFrame(self)
        self.real_time_box.setStyleSheet(""" 
            background-color: #36454F;
            border-radius: 10px;
            padding: 20px;
        """)
        self.real_time_box.setFixedWidth(900)  # Adjust the width of the real-time detection box
        self.real_time_box.setFixedHeight(700)  # Adjust the height of the real-time detection box
        right_layout = QVBoxLayout(self.real_time_box)
        self.real_time_label = QLabel("Real-time Detection", self.real_time_box)
        self.real_time_label.setStyleSheet("font-size: 22px; color: white; font-weight: bold;")
        self.real_time_label.setAlignment(Qt.AlignCenter)
        self.proceed_button = CustomButton1("Proceed", self.real_time_box)
        self.proceed_button.setStyleSheet("background-color: #2c2f35; color: white; padding: 30px; font-size: 18px; border-radius: 15px; width: 250px;")
        self.proceed_button.clicked.connect(self.show_live_detection_page)
        right_layout.addWidget(self.real_time_label)
        right_layout.addWidget(self.proceed_button)
        right_layout.setAlignment(Qt.AlignCenter)

        # Add both boxes to the main layout (center them)
        main_layout.addWidget(self.submit_video_box)
        main_layout.addWidget(self.real_time_box)
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignCenter)

        # Set the window size
        self.resize(800, 600)


    def show_upload_form(self):
        self.upload_form = UploadForm()
        self.upload_form.exec_()

    def show_live_detection_page(self):
        # Navigate to the live detection page when the user clicks "Proceed"
        self.live_detection_page = LiveDetectionPage()
        self.live_detection_page.show()
        self.close()  # Close the current page

class DetectionTypePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Veloci")

        self.setWindowIcon(QIcon(resource_path("assets/logo.png")))


        # Set background color for the detection type page
        self.setStyleSheet("background-color: #2c2f35;")  # Dark green background color

        # Create the layout for the two boxes (submit video and real-time detection)
        main_layout = QHBoxLayout(self)

        # Left side: Submit Video Recording
        self.submit_video_box = QFrame(self)
        self.submit_video_box.setStyleSheet(""" 
            background-color: #36454F;
            border-radius: 10px;
            padding: 20px;
            margin-right: 20px;
        """)
        self.submit_video_box.setFixedWidth(900)  # Adjust the width of the video submission box
        self.submit_video_box.setFixedHeight(700)  # Adjust the height of the video submission box
        left_layout = QVBoxLayout(self.submit_video_box)
        self.submit_video_label = QLabel("Submit Video Recording", self.submit_video_box)
        self.submit_video_label.setStyleSheet("font-size: 22px; color: white; font-weight: bold;")
        self.submit_video_label.setAlignment(Qt.AlignCenter)
        self.upload_button = CustomButton1("Upload", self.submit_video_box)
        self.upload_button.setStyleSheet("background-color: #2c2f35; color: white; padding: 30px; font-size: 18px; border-radius: 15px; width: 250px;")
        self.upload_button.clicked.connect(self.show_upload_form)
        left_layout.addWidget(self.submit_video_label)
        left_layout.addWidget(self.upload_button)
        left_layout.setAlignment(Qt.AlignCenter)

        # Right side: Real-time Detection
        self.real_time_box = QFrame(self)
        self.real_time_box.setStyleSheet(""" 
            background-color: #36454F;
            border-radius: 10px;
            padding: 20px;
        """)
        self.real_time_box.setFixedWidth(900)  # Adjust the width of the real-time detection box
        self.real_time_box.setFixedHeight(700)  # Adjust the height of the real-time detection box
        right_layout = QVBoxLayout(self.real_time_box)
        self.real_time_label = QLabel("Real-time Detection", self.real_time_box)
        self.real_time_label.setStyleSheet("font-size: 22px; color: white; font-weight: bold;")
        self.real_time_label.setAlignment(Qt.AlignCenter)
        self.proceed_button = CustomButton1("Proceed", self.real_time_box)
        self.proceed_button.setStyleSheet("background-color: #2c2f35; color: white; padding: 30px; font-size: 18px; border-radius: 15px; width: 250px;")
        self.proceed_button.clicked.connect(self.show_live_detection_page)
        right_layout.addWidget(self.real_time_label)
        right_layout.addWidget(self.proceed_button)
        right_layout.setAlignment(Qt.AlignCenter)

        # Add both boxes to the main layout (center them)
        main_layout.addWidget(self.submit_video_box)
        main_layout.addWidget(self.real_time_box)
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignCenter)

        # Make the window full screen
        self.showFullScreen()  # Open in full-screen mode

    def show_upload_form(self):
        self.upload_form = UploadForm(self)
        self.upload_form.exec_()

    def show_live_detection_page(self):
        # Navigate to the live detection page when the user clicks "Proceed"
        self.live_detection_page = LiveDetectionPage()
        self.live_detection_page.show()
        self.close()  # Close the current page

    def keyPressEvent(self, event):
        """Override the keyPressEvent to listen for the Esc key."""
        if event.key() == Qt.Key_Escape:
            self.close()  # Close the window when Esc is pressed
        elif event.key() == Qt.Key_M:  # You can also add functionality to minimize
            self.showMinimized()  # Minimize the window when M is pressed



class UploadForm(QDialog):
    def __init__(self, detection_type_page):
        super().__init__()
        self.detection_type_page = detection_type_page
        self.setWindowTitle("Upload Video")

        self.setWindowIcon(QIcon(resource_path("assets/logo.png")))

        self.setStyleSheet("background-color: #36454F;")  # Background

        # Layouts
        form_layout = QFormLayout()
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(15)

        # Choose File Button
        self.upload_button = CustomButton3("Choose a File", self)
        self.upload_button.setStyleSheet("""
            background-color: #2c2f35;
            color: white;
            padding: 12px 20px;
            font-size: 16px;
            border-radius: 10px;
        """)
        self.upload_button.clicked.connect(self.choose_file)

        # File Name Label
        self.video_file_label = QLabel("No file selected", self)
        self.video_file_label.setStyleSheet("""
            color: #FFFFFF;
            font-size: 14px;
        """)
        form_layout.addRow(self.upload_button, self.video_file_label)

        # Upload Button (Manual trigger)
        self.process_button = CustomButton3("Upload", self)
        self.process_button.setStyleSheet("""
            background-color: #2c2f35;
            color: white;
            padding: 12px 20px;
            font-size: 16px;
            border-radius: 10px;
        """)
        self.process_button.setEnabled(False)
        self.process_button.clicked.connect(self.upload_and_process)
        form_layout.addRow(self.process_button)

        # Progress Bar
        processing_label = QLabel("Processing:", self)
        processing_label.setStyleSheet("""
            font-size: 14px;
            color: #FFFFFF;
        """)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                font-size: 14px;
                color: #FFFFFF;
                background-color: #555;
                border-radius: 5px;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #008CBA;
                width: 10px;
            }
            QProgressBar::text {
                color: white;
            }
        """)
        form_layout.addRow(processing_label, self.progress_bar)

        # Set Layout
        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        self.setLayout(layout)

        # Set Window Size + Center
        self.resize(400, 250)
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())

        # Initialize the model (ensure the correct path)
        model_path = resource_path("models/best_yolov11-L.pt")
        self.model = YOLO(model_path)  # Load the model

        if torch.cuda.is_available():
            self.model = self.model.to('cuda')
            print("Model moved to GPU.")
        else:
            print("CUDA not available, using CPU.")

    def choose_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Choose Video File", "", "Video Files (*.mp4 *.avi *.mov)")
        if file:
            self.video_file_label.setText(file)
            self.selected_file = file
            self.process_button.setEnabled(True)  # Enable Upload button

    def upload_and_process(self):
        if hasattr(self, "selected_file"):
            self.progress_bar.setValue(50)
            print(f"Processing video: {self.selected_file}")

            # Simulate processing
            self.progress_bar.setValue(100)
            print("Video processed successfully!")

            if self.detection_type_page:
                self.detection_type_page.close()  # Close DetectionTypePage

            self.display_detection_results(self.selected_file)

    def display_detection_results(self, video_file):
        self.results_page = ResultsPage(video_file, self.model)
        self.results_page.show()
        self.close()

    def keyPressEvent(self, event):
        """Override the keyPressEvent to listen for the Esc key."""
        if event.key() == Qt.Key_Escape:
            self.close()  # Close the window when Esc is pressed
        elif event.key() == Qt.Key_M:  # You can also add functionality to minimize
            self.showMinimized()  # Minimize the window when M is pressed


class ResultsPage(QWidget):
    def __init__(self, video_file, model):
        super().__init__()
        self.setWindowTitle("Veloci")
        self.setWindowIcon(QIcon(resource_path("assets/logo.png")))


        # Save the model
        self.model = model
        
        # Save the video file as an attribute
        self.video_file = video_file  # Store video_file as an instance attribute
        
        # Set background color
        self.setStyleSheet("background-color: #2c2f35;")

        # Create a label to show the video with bounding boxes
        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("border: 2px solid #ffffff; border-radius: 10px;")
        self.video_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Initialize the video capture
        self.cap = cv2.VideoCapture(video_file)
        if not self.cap.isOpened():
            print("Error: Couldn't open video file.")
            return
        
        # Set the QLabel to a fixed size (640x480)
        self.video_label.setFixedWidth(1800)
        self.video_label.setFixedHeight(925)

        # Add Generate Report (CSV) button
        self.download_report_button = QPushButton("Generate Report (CSV)", self)
        self.download_report_button.setStyleSheet(""" 
            QPushButton {
                background-color: #8C6D9D;  /* Lavender grey */
                color: white;
                padding: 12px 20px;
                font-size: 18px;
                border-radius: 25px;
                width: 220px;
            }
            QPushButton:hover {
                background-color: #75588A;  /* Darker lavender grey */
            }
            """)
        self.download_report_button.clicked.connect(self.generate_report)

        # Add Generate Report (PDF) button
        self.download_pdf_button = QPushButton("Generate Report (PDF)", self)
        self.download_pdf_button.setStyleSheet(""" 
            QPushButton {
                background-color: #5A7539;  /* Muted olive green */
                color: white;
                padding: 12px 20px;
                font-size: 18px;
                border-radius: 25px;
                width: 220px;
            }
            QPushButton:hover {
                background-color: #4A6430;  /* Darker olive green */
            }
        """)
        self.download_pdf_button.clicked.connect(self.generate_pdf_report)

        # Add Restart button (matching the Home button color)
        self.restart_button = QPushButton("Restart", self)
        self.restart_button.setStyleSheet(""" 
            QPushButton {
                background-color: #5E6D7A;  /* Slate grey */
                color: white;
                padding: 12px 20px;
                font-size: 18px;
                border-radius: 25px;
                width: 220px;
            }
            QPushButton:hover {
                background-color: #4A5A64;  /* Darker slate grey */
            }
        """)
        self.restart_button.clicked.connect(self.restart)

        # Add Replay button with an image icon
        self.replay_button = QPushButton(self)
        replay_icon = QPixmap(resource_path("assets/replay.png"))  # Add your replay icon image here
        self.replay_button.setIcon(QIcon(replay_icon))
        self.replay_button.setIconSize(QSize(50, 50))  # Adjust the icon size
        self.replay_button.setStyleSheet("""
            QPushButton {
                background-color: #ADD8E6;  /* Default color */
                border: none;
            }
            QPushButton:hover {
                background-color: #87B3C2;  /* Darker shade of #ADD8E6 */
            }
        """)
        self.replay_button.clicked.connect(self.replay_video)  # Connect the replay button to the replay method

        # Create layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.download_report_button)
        button_layout.addWidget(self.download_pdf_button)
        button_layout.addWidget(self.replay_button)  # Add Replay Button between the two
        button_layout.addWidget(self.restart_button)
        button_layout.setSpacing(20)

        # Layout setup for result page
        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addLayout(button_layout)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)
        self.setLayout(layout)

        # Make the window full screen
        self.showFullScreen()  # Open in full-screen mode

        # Initialize the video capture
        self.cap = cv2.VideoCapture(video_file)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update frame every 30 ms

        self.summary_data = []  # List to store the detection results

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.cap.release()
            self.timer.stop()
            return
        
        # Run detection with YOLO model
        results = self.model(frame)  # Use the passed model for inference
        annotated_frame = results[0].plot()  # Draw bounding boxes

        # Capture detection results and add to summary
        detections = results[0].boxes.cls.tolist()
        confidences = results[0].boxes.conf.tolist()  # Capture the confidence scores
        if detections:
            labels = [self.model.names[int(cls)] for cls in detections]
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            for i, label in enumerate(labels):
                confidence = confidences[i]  # Get the confidence for each detection
                self.summary_data.append([now, label, confidence])  # Add confidence to summary

        # Convert the frame to RGB
        rgb_image = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

        # Update the label with the new frame
        self.video_label.setPixmap(QPixmap.fromImage(qt_image))

    from datetime import datetime

    def generate_report(self):
        # Allow the user to choose where to save the CSV file
        file_name, _ = QFileDialog.getSaveFileName(self, "Save CSV File", "", "CSV Files (*.csv)")
        if file_name:
            # Write the summary data to the CSV file
            with open(file_name, "w", newline="") as file:
                writer = csv.writer(file)

                video_name = os.path.basename(self.video_file)  #This defines video_name properly
                generated_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Add report title header
                writer.writerow(["","Road Damage Detection Report", ""])
                writer.writerow(["",f"Report Generated on: {generated_datetime}", ""])
                writer.writerow(["",f"Source video: {video_name}", ""])
                writer.writerow([])  # Blank line for spacing

                if not self.summary_data:

                    # No detections found
                    writer.writerow(["No road damage was detected during the analysis of the submitted video recording."])
                    writer.writerow([])  # Blank line for spacing
                    print(f"No detections found. CSV report saved to {file_name}")
                    return
                
                # Gather unique road damage types
                detected_damage_types = set(row[1] for row in self.summary_data)

                # Write detected damage types
                writer.writerow([f"Detected Road Damage: {', '.join(detected_damage_types)}"])
                writer.writerow([])  # Blank line for spacing

                writer.writerow([])  # Add an empty row for spacing
                writer.writerow(["Timestamp(s)", "Label", "Confidence"])

                for row in self.summary_data:
                    timestamp = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
                    writer.writerow([f'"{timestamp}"', row[1], round(row[2] * 100, 2)])
                    
            print(f"CSV Report saved to {file_name}")

    def generate_pdf_report(self):
        from PyQt5.QtWidgets import QFileDialog
        from fpdf import FPDF
        from datetime import datetime
        import os

        # Let user choose save location
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(None, "Save PDF File", "", "PDF Files (*.pdf)", options=options)

        if file_name:
            video_name = os.path.basename(self.video_file)
            generated_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()

            # Report title
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, "Road Damage Detection Report", ln=True, align='C')
            pdf.ln(5)

            # Metadata
            pdf.set_font("Arial", size=11)
            pdf.cell(200, 10, f"Report Generated on: {generated_datetime}", ln=True, align='C')
            pdf.cell(200, 10, f"Source video: {video_name}", ln=True, align='C')
            pdf.ln(10)

            # Handle empty or populated summary_data
            if not self.summary_data:
                # No damage detected message
                pdf.set_font("Arial", 'I', 12)
                pdf.multi_cell(0, 10, "No road damage was detected during the analysis of the submitted video recording.", align='C')
            else:
                # Gather unique road damage types
                detected_damage_types = set(row[1] for row in self.summary_data)

                # Write detected damage types
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, f"Detected Road Damage: {', '.join(detected_damage_types)}", align='C')
                pdf.ln(10)

                # Table header
                pdf.set_font("Arial", size=10)
                col_widths = [60, 60, 30]
                start_x = (210 - sum(col_widths)) / 2
                pdf.set_x(start_x)

                pdf.cell(60, 10, "Timestamp(s)", border=1, align='C')
                pdf.cell(60, 10, "Label", border=1, align='C')
                pdf.cell(30, 10, "Confidence", border=1, align='C')
                pdf.ln(10)

                for row in self.summary_data:
                    timestamp = row[0]
                    label = row[1]
                    confidence = f"{round(row[2] * 100, 2)}%"

                    pdf.set_x(start_x)
                    pdf.cell(60, 10, str(timestamp), border=1, align='C')
                    pdf.cell(60, 10, str(label), border=1, align='C')
                    pdf.cell(30, 10, str(confidence), border=1, align='C')
                    pdf.ln(10)

            # Save PDF
            pdf.output(file_name)
            print(f"PDF report saved to {file_name}")


    def restart(self):
        # Stop the video capture and timer to stop the current video processing
        self.cap.release()
        self.timer.stop()
        
        self.close()
        self.home_page = DetectionTypePage()
        self.home_page.show()

    def replay_video(self):
        """Restart the video from the beginning"""
        # Release the current capture and reset it
        self.cap.release()
        self.cap = cv2.VideoCapture(self.video_file)  # Use the stored `video_file` attribute
        self.timer.start(30)  # Restart the frame update4

    def keyPressEvent(self, event):
        """Override the keyPressEvent to listen for the Esc key."""
        if event.key() == Qt.Key_Escape:
            self.close()  # Close the window when Esc is pressed
        elif event.key() == Qt.Key_M:  # You can also add functionality to minimize
            self.showMinimized()  # Minimize the window when M is pressed



class LiveDetectionPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Veloci")
        self.setWindowIcon(QIcon(resource_path("assets/logo.png")))

        # Set background color for live detection page
        self.setStyleSheet("background-color: #2c2f35;")  # Dark green background color

        # Initialize summary_data to store detection results
        self.summary_data = []

        # Add image label to display webcam feed
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 6px solid #36454F; border-radius: 40px;")

        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setFixedWidth(1800)
        self.image_label.setFixedHeight(925)

        # Add Start Detection button
        self.start_button = QPushButton("Start Detection", self)
        self.start_button.setStyleSheet(""" 
            QPushButton {
                background-color: #4A6D6E;
                color: white;
                padding: 12px 20px;
                font-size: 18px;
                border-radius: 25px;
                width: 220px;
            }
            QPushButton:hover {
                background-color: #3B5854;
            }
        """)
        self.start_button.clicked.connect(self.start_detection)

        # Add Stop Detection button
        self.stop_button = QPushButton("Stop Detection", self)
        self.stop_button.setStyleSheet(""" 
            QPushButton {
                background-color: #D32F2F;
                color: white;
                padding: 12px 20px;
                font-size: 18px;
                border-radius: 25px;
                width: 220px;
            }
            QPushButton:hover {
                background-color: #B12C2C;
            }
        """)
        self.stop_button.clicked.connect(self.stop_detection)

        # Add Generate Report (CSV) button
        self.generate_report_button = QPushButton("Generate Report (CSV)", self)
        self.generate_report_button.setStyleSheet(""" 
            QPushButton {
                background-color: #8C6D9D;
                color: white;
                padding: 12px 20px;
                font-size: 18px;
                border-radius: 25px;
                width: 220px;
            }
            QPushButton:hover {
                background-color: #75588A;
            }
        """)
        self.generate_report_button.clicked.connect(self.generate_report)

        # Add Generate Report (PDF) button
        self.generate_pdf_report_button = QPushButton("Generate Report (PDF)", self)
        self.generate_pdf_report_button.setStyleSheet(""" 
            QPushButton {
                background-color: #5A7539;
                color: white;
                padding: 12px 20px;
                font-size: 18px;
                border-radius: 25px;
                width: 220px;
            }
            QPushButton:hover {
                background-color: #4A6430;
            }
        """)
        self.generate_pdf_report_button.clicked.connect(self.generate_pdf_report)

        # Add Home button to go back to the homepage
        self.home_button = QPushButton("Restart", self)
        self.home_button.setStyleSheet(""" 
            QPushButton {
                background-color: #5E6D7A;
                color: white;
                padding: 12px 20px;
                font-size: 18px;
                border-radius: 25px;
                width: 220px;
            }
            QPushButton:hover {
                background-color: #4A5A64;
            }
        """)
        self.home_button.clicked.connect(self.go_home)

        # Layout setup for the buttons (arranging buttons horizontally)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.generate_report_button)
        button_layout.addWidget(self.generate_pdf_report_button)
        button_layout.addWidget(self.home_button)
        button_layout.setSpacing(20)

        # Layout setup for the live detection page
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addLayout(button_layout)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)
        self.setLayout(layout)

        # Initialize webcam and timer
        self.cap = cv2.VideoCapture(0)  # Use camera 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update frame every 30 ms

        # YOLO model setup (load the trained model)
        model_path = resource_path("models/best_yolov11-L.pt")
        self.model = YOLO(model_path)

        if torch.cuda.is_available():
            self.model = self.model.to('cuda')  # Move model to GPU if available
            print("Model moved to GPU.")
        else:
            print("CUDA not available, using CPU.")

        self.is_detection_started = False  # To track if detection has started

        # Make the window full screen
        self.showFullScreen()

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        # Perform detection if detection has started
        if self.is_detection_started:
            results = self.model(frame)  # Run the detection using YOLO model
            annotated = results[0].plot()  # Get the annotated frame with bounding boxes

            # Extract detections and confidence
            detections = results[0].boxes.cls.tolist()
            confidences = results[0].boxes.conf.tolist()  # Capture the confidence scores
            if detections:
                labels = [self.model.names[int(cls)] for cls in detections]
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                for i, label in enumerate(labels):
                    confidence = confidences[i]  # Get the confidence for each detection
                    self.summary_data.append([now, label, confidence])  # Add to summary data

        else:
            annotated = frame  # If no detection is started, just show the raw camera feed

        # Resize and display the frame
        frame_height, frame_width = annotated.shape[:2]
        new_width = 2200
        aspect_ratio = frame_width / frame_height
        new_height = int(new_width / aspect_ratio)
        resized_frame = cv2.resize(annotated, (new_width, new_height))

        rgb_image = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

        self.image_label.setPixmap(QPixmap.fromImage(qt_image))

    def start_detection(self):
        """Start the detection when the user clicks 'Start Detection'"""
        self.is_detection_started = True
        self.start_button.setEnabled(False)  # Disable the Start button after detection starts
        self.summary_data = []  # Clear previous data when detection starts
        self.detection_start_time = datetime.now()  # Record the start time
        print(f"Detection started at: {self.detection_start_time}")

    def stop_detection(self):
        """Stop the detection when the user clicks 'Stop Detection'"""
        self.is_detection_started = False
        self.start_button.setEnabled(True)  # Enable the Start button to allow restarting detection
        self.detection_end_time = datetime.now()  # Record the end time
        print(f"Detection stopped at: {self.detection_end_time}")

    def generate_pdf_report(self):
        """Generate PDF report with real start and end time"""
        if not self.summary_data:
            print("No detections to report.")
            return

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save PDF File", "", "PDF Files (*.pdf)", options=options)

        if file_name:
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()

            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, "Road Damage Detection Report", ln=True, align='C')
            pdf.ln(10)

            pdf.set_font("Arial", size=10)
            col_widths = [60, 60, 30]
            start_x = (210 - sum(col_widths)) / 2
            pdf.set_x(start_x)

            pdf.cell(60, 10, "Timestamp(s)", border=1, align='C')
            pdf.cell(60, 10, "Label", border=1, align='C')
            pdf.cell(30, 10, "Confidence", border=1, align='C')
            pdf.ln(10)

            # Add session start and end times to the PDF
            start = self.detection_start_time.strftime("%Y-%m-%d %H:%M:%S") if self.detection_start_time else "N/A"
            end = self.detection_end_time.strftime("%Y-%m-%d %H:%M:%S") if self.detection_end_time else "N/A"
            pdf.cell(200, 10, f"Live inspection session started at: {start}", ln=True, align='C')
            pdf.cell(200, 10, f"Live inspection session ended at: {end}", ln=True, align='C')
            pdf.ln(10)

            for row in self.summary_data:
                timestamp = row[0]
                label = row[1]
                confidence = f"{round(row[2] * 100, 2)}%"  # Convert confidence to percentage

                pdf.set_x(start_x)
                pdf.cell(60, 10, str(timestamp), border=1, align='C')
                pdf.cell(60, 10, str(label), border=1, align='C')
                pdf.cell(30, 10, str(confidence), border=1, align='C')
                pdf.ln(10)

            pdf.output(file_name)
            print(f"PDF report saved to {file_name}")

class LiveDetectionPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Veloci")
        self.setWindowIcon(QIcon(resource_path("assets/logo.png")))

        # Set background color for live detection page
        self.setStyleSheet("background-color: #2c2f35;")  # Dark green background color

        # Initialize summary_data to store detection results
        self.summary_data = []

        # Add image label to display webcam feed
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 6px solid #36454F; border-radius: 40px;")

        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setFixedWidth(1800)
        self.image_label.setFixedHeight(925)

        # Add Start Detection button
        self.start_button = QPushButton("Start Detection", self)
        self.start_button.setStyleSheet(""" 
            QPushButton {
                background-color: #4A6D6E;
                color: white;
                padding: 12px 20px;
                font-size: 18px;
                border-radius: 25px;
                width: 220px;
            }
            QPushButton:hover {
                background-color: #3B5854;
            }
        """)
        self.start_button.clicked.connect(self.start_detection)

        # Add Stop Detection button
        self.stop_button = QPushButton("Stop Detection", self)
        self.stop_button.setStyleSheet(""" 
            QPushButton {
                background-color: #D32F2F;
                color: white;
                padding: 12px 20px;
                font-size: 18px;
                border-radius: 25px;
                width: 220px;
            }
            QPushButton:hover {
                background-color: #B12C2C;
            }
        """)
        self.stop_button.clicked.connect(self.stop_detection)

        # Add Generate Report (CSV) button
        self.generate_report_button = QPushButton("Generate Report (CSV)", self)
        self.generate_report_button.setStyleSheet(""" 
            QPushButton {
                background-color: #8C6D9D;
                color: white;
                padding: 12px 20px;
                font-size: 18px;
                border-radius: 25px;
                width: 220px;
            }
            QPushButton:hover {
                background-color: #75588A;
            }
        """)
        self.generate_report_button.clicked.connect(self.generate_report)

        # Add Generate Report (PDF) button
        self.generate_pdf_report_button = QPushButton("Generate Report (PDF)", self)
        self.generate_pdf_report_button.setStyleSheet(""" 
            QPushButton {
                background-color: #5A7539;
                color: white;
                padding: 12px 20px;
                font-size: 18px;
                border-radius: 25px;
                width: 220px;
            }
            QPushButton:hover {
                background-color: #4A6430;
            }
        """)
        self.generate_pdf_report_button.clicked.connect(self.generate_pdf_report)

        # Add Home button to go back to the homepage
        self.home_button = QPushButton("Restart", self)
        self.home_button.setStyleSheet(""" 
            QPushButton {
                background-color: #5E6D7A;
                color: white;
                padding: 12px 20px;
                font-size: 18px;
                border-radius: 25px;
                width: 220px;
            }
            QPushButton:hover {
                background-color: #4A5A64;
            }
        """)
        self.home_button.clicked.connect(self.go_home)

        # Layout setup for the buttons (arranging buttons horizontally)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.generate_report_button)
        button_layout.addWidget(self.generate_pdf_report_button)
        button_layout.addWidget(self.home_button)
        button_layout.setSpacing(20)

        # Layout setup for the live detection page
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addLayout(button_layout)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)
        self.setLayout(layout)

        # Initialize webcam and timer
        self.cap = cv2.VideoCapture(0)  # Use camera 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update frame every 30 ms

        # YOLO model setup (load the trained model)
        model_path = resource_path("models/best_yolov11-L.pt")
        self.model = YOLO(model_path)

        if torch.cuda.is_available():
            self.model = self.model.to('cuda')  # Move model to GPU if available
            print("Model moved to GPU.")
        else:
            print("CUDA not available, using CPU.")

        self.is_detection_started = False  # To track if detection has started

        # Disable the "Generate Report" buttons initially
        self.stop_button.setEnabled(False)
        self.generate_report_button.setEnabled(False)
        self.generate_pdf_report_button.setEnabled(False)

        # Make the window full screen
        self.showFullScreen()

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        # Perform detection if detection has started
        if self.is_detection_started:
            results = self.model(frame)  # Run the detection using YOLO model
            annotated = results[0].plot()  # Get the annotated frame with bounding boxes

            # Extract detections and confidence
            detections = results[0].boxes.cls.tolist()
            confidences = results[0].boxes.conf.tolist()  # Capture the confidence scores
            if detections:
                labels = [self.model.names[int(cls)] for cls in detections]
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                for i, label in enumerate(labels):
                    confidence = confidences[i]  # Get the confidence for each detection
                    self.summary_data.append([now, label, confidence])  # Add to summary data

        else:
            annotated = frame  # If no detection is started, just show the raw camera feed

        # Resize and display the frame
        frame_height, frame_width = annotated.shape[:2]
        new_width = 2200
        aspect_ratio = frame_width / frame_height
        new_height = int(new_width / aspect_ratio)
        resized_frame = cv2.resize(annotated, (new_width, new_height))

        rgb_image = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

        self.image_label.setPixmap(QPixmap.fromImage(qt_image))

    def start_detection(self):
        """Start the detection when the user clicks 'Start Detection'"""
        self.is_detection_started = True
        self.start_button.setEnabled(False)  # Disable the Start button after detection starts
        self.summary_data = []  # Clear previous data when detection starts
        self.detection_start_time = datetime.now()  # Record the start time
        print(f"Detection started at: {self.detection_start_time}")

        # Disable Generate Report buttons while detection is in progress
        self.stop_button.setEnabled(True)
        self.generate_report_button.setEnabled(False)
        self.generate_pdf_report_button.setEnabled(False)

    def stop_detection(self):
        """Stop the detection when the user clicks 'Stop Detection'"""
        self.is_detection_started = False
        self.start_button.setEnabled(True)  # Enable the Start button to allow restarting detection
        self.detection_end_time = datetime.now()  # Record the end time
        print(f"Detection stopped at: {self.detection_end_time}")

        # Enable Generate Report buttons after detection has stopped
        self.generate_report_button.setEnabled(True)
        self.generate_pdf_report_button.setEnabled(True)

    def generate_pdf_report(self):
        """Generate PDF report with real start and end time, even if no damage is detected"""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save PDF File", "", "PDF Files (*.pdf)", options=options)

        if file_name:
            # Create PDF
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()

            # Title
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, "Road Damage Detection Report", ln=True, align='C')
            pdf.ln(10)

            # Metadata (including report generation time and session times)
            generated_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            pdf.set_font("Arial", size=10)
            pdf.cell(200, 10, f"Report Generated on: {generated_datetime}", ln=True, align='C')
            pdf.ln(3)

            # Session start and end times
            start = self.detection_start_time.strftime("%Y-%m-%d %H:%M:%S") if self.detection_start_time else "N/A"
            end = self.detection_end_time.strftime("%Y-%m-%d %H:%M:%S") if self.detection_end_time else "N/A"
            pdf.cell(200, 10, f"Live inspection session started at: {start}", ln=True, align='C')
            pdf.cell(200, 10, f"Live inspection session ended at: {end}", ln=True, align='C')
            pdf.ln(10)

            # Gather unique road damage types
            if self.summary_data:
                detected_damage_types = set(row[1] for row in self.summary_data)

                # Display detected damage types
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, f"Detected Road Damage: {', '.join(detected_damage_types)}", align='C')
                pdf.ln(10)

            # Check if no damage detected
            if not self.summary_data:
                pdf.set_font("Arial", 'I', 12)
                pdf.multi_cell(0, 10, "No road damage was detected during the live inspection session.", align='C')
            else:
                # Table headers for detected damage (if any)
                pdf.set_font("Arial", size=10)
                col_widths = [60, 60, 30]
                start_x = (210 - sum(col_widths)) / 2
                pdf.set_x(start_x)

                pdf.cell(60, 10, "Timestamp(s)", border=1, align='C')
                pdf.cell(60, 10, "Label", border=1, align='C')
                pdf.cell(30, 10, "Confidence", border=1, align='C')
                pdf.ln(10)

                # Add detected data rows
                for row in self.summary_data:
                    timestamp = row[0]
                    label = row[1]
                    confidence = f"{round(row[2] * 100, 2)}%"  # Convert confidence to percentage

                    pdf.set_x(start_x)
                    pdf.cell(60, 10, str(timestamp), border=1, align='C')
                    pdf.cell(60, 10, str(label), border=1, align='C')
                    pdf.cell(30, 10, str(confidence), border=1, align='C')
                    pdf.ln(10)

            # Save PDF to the selected location
            pdf.output(file_name)
            print(f"PDF report saved to {file_name}")


    def generate_report(self):
        """Generate CSV report for the session"""
        file_name, _ = QFileDialog.getSaveFileName(self, "Save CSV File", "", "CSV Files (*.csv)")
        if file_name:
            with open(file_name, "w", newline="") as file:
                writer = csv.writer(file)

                start = self.detection_start_time.strftime("%Y-%m-%d %H:%M:%S") if self.detection_start_time else "N/A"
                end = self.detection_end_time.strftime("%Y-%m-%d %H:%M:%S") if self.detection_end_time else "N/A"
                generated_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Title
                writer.writerow(["", "Road Damage Detection Report", "", "", ""])
                writer.writerow([])

                # Session Times
                writer.writerow([f"Report Generated on: {generated_datetime}", "", "", ""])
                writer.writerow([f"Live inspection session started at: {start}"])
                writer.writerow([f"Live inspection session ended at: {end}"])
                writer.writerow([])

                # Gather unique road damage types
                if self.summary_data:
                    detected_damage_types = set(row[1] for row in self.summary_data)

                    # Write detected damage types
                    writer.writerow([f"Detected Road Damage: {', '.join(detected_damage_types)}"])
                    writer.writerow([])

                # No detections
                if not self.summary_data:
                    writer.writerow(["No road damage was detected during the live inspection session."])
                    print(f"No detections found. CSV report saved to {file_name}")
                    return

                # Detected
                writer.writerow(["Timestamp(s)", "Label", "Confidence"])
                for row in self.summary_data:
                    timestamp = "'" + datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
                    writer.writerow([timestamp, row[1], round(row[2] * 100, 2)])

            print(f"CSV Report saved to {file_name}")

    def go_home(self):
        """Navigate back to the homepage and stop any running detection"""
        self.cap.release()  # Release the camera
        self.timer.stop()  # Stop the frame updates
        self.close()  # Close the live detection page
        self.home_page = DetectionTypePage()  # Show the home page again
        self.home_page.show()
 
    def keyPressEvent(self, event):
        """Override the keyPressEvent to listen for the Esc key."""
        if event.key() == Qt.Key_Escape:
            self.close()  # Close the window when Esc is pressed
        elif event.key() == Qt.Key_M:  # You can also add functionality to minimize
            self.showMinimized()  # Minimize the window when M is pressed

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YOLOApp()
    window.show()
    sys.exit(app.exec_())
