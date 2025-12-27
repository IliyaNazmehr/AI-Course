"""
Object detection module using YOLOv8.
"""

from ultralytics import YOLO
import cv2
import pandas as pd
from typing import Optional, Tuple
import numpy as np


class ObjectDetector:
    """YOLOv8 based object detector with comprehensive features."""
    
    def __init__(self, model_name: str = 'yolov8n.pt') -> None:
        """
        Initialize the object detector.
        
        Args:
            model_name: Name of the YOLO model file
        """
        self.model = YOLO(model_name)
        self.results = None
        self.model_name = model_name
    
    def detect_objects(self, image_path: str) -> np.ndarray:
        """
        Detect objects in an image and return annotated image.
        
        Args:
            image_path: Path to the input image
            
        Returns:
            Annotated image with bounding boxes
            
        Raises:
            FileNotFoundError: If image path is invalid
            RuntimeError: If detection fails
        """
        try:
            # Perform object detection
            self.results = self.model(image_path)
            
            # Draw bounding boxes on image
            annotated_image = self.results[0].plot()
            
            # Convert BGR to RGB for display
            return cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
            
        except Exception as e:
            raise RuntimeError(f"Object detection failed: {str(e)}")
    
    def get_detection_data(self) -> pd.DataFrame:
        """
        Extract detection results as structured DataFrame.
        
        Returns:
            DataFrame containing detection information
        """
        if self.results is None:
            return pd.DataFrame()
        
        detection_data = []
        
        for result in self.results:
            for box in result.boxes:
                detection_data.append(self._parse_detection_box(box, result.names))
        
        return pd.DataFrame(detection_data)
    
    def _parse_detection_box(self, box, class_names: dict) -> dict:
        """
        Parse individual detection box data.
        
        Args:
            box: Detection box object
            class_names: Dictionary of class names
            
        Returns:
            Dictionary of box properties
        """
        # Extract coordinates
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        
        # Calculate dimensions
        width = x2 - x1
        height = y2 - y1
        
        # Get class information
        class_id = int(box.cls[0])
        class_name = class_names[class_id]
        
        # Get confidence score
        confidence = float(box.conf[0])
        
        return {
            'class': class_name,
            'confidence': confidence,
            'x_min': x1,
            'y_min': y1,
            'x_max': x2,
            'y_max': y2,
            'width': width,
            'height': height,
            'area': width * height
        }
    
    def get_model_info(self) -> dict:
        """Get information about the loaded model."""
        return {
            'model_name': self.model_name,
            'model_type': 'YOLOv8',
            'classes': 80 if hasattr(self.model, 'names') else 'Unknown'
        }