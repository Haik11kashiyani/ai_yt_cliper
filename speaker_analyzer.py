import cv2
import mediapipe as mp
import numpy as np

class SpeakerAnalyzer:
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=1, min_detection_confidence=0.5
        )

    def detect_primary_speaker(self, video_path, sample_interval=30):
        """
        Scans the video to find where the main face is.
        Returns the x-center coordinate (0.0 to 1.0) of the speaker.
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return 0.5  # Default to center if video fails

        frame_count = 0
        face_centers = []

        while True:
            success, frame = cap.read()
            if not success:
                break

            # Only analyze every Nth frame to save time
            if frame_count % sample_interval == 0:
                results = self.face_detection.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                
                if results.detections:
                    # Find the biggest face (closest to camera)
                    largest_face = max(results.detections, key=lambda d: d.location_data.relative_bounding_box.width)
                    bbox = largest_face.location_data.relative_bounding_box
                    center_x = bbox.xmin + (bbox.width / 2)
                    face_centers.append(center_x)

            frame_count += 1

        cap.release()

        if not face_centers:
            print("⚠️ No faces detected. Defaulting to center crop.")
            return 0.5

        # Return the average position of the speaker
        return np.mean(face_centers)

    def get_speakers_layout(self, video_path):
        """
        Determines if we should use single view or split view.
        (Simplified for stability)
        """
        # For now, we will return a generic map. 
        # You can expand this to detect 2 people later.
        return {
            "type": "single_speaker",
            "center": self.detect_primary_speaker(video_path)
        }
