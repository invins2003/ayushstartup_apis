import requests
from io import BytesIO
import cv2
import numpy as np
import pytesseract
import re

class OCRProcessor:
    """Class to handle OCR processing for extracting Aadhaar and PAN details."""

    def __init__(self):
        pass

    def preprocess_image(self, image):
        """Preprocess the image for better OCR results."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)  # Denoise the image
        smoothed = cv2.GaussianBlur(denoised, (3, 3), 0)  # Apply Gaussian Blur
        return smoothed

    def extract_aadhaar_details(self, image):
        """Extract Aadhaar details using OCR."""
        smoothed = self.preprocess_image(image)
        thresh = cv2.adaptiveThreshold(smoothed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 13, 3)
        text = pytesseract.image_to_string(thresh)

        # Patterns to identify details
        aadhaar_pattern = r"\b(\d{4}\s\d{4}\s\d{4})\b"

        # Extracting details
        aadhaar_match = re.search(aadhaar_pattern, text)
        aadhaar_number = aadhaar_match.group(0) if aadhaar_match else "Not Found"

        return {
            "aadhaar_number": aadhaar_number
        }

    def extract_pan_details(self, image):
        """Extract PAN card details using OCR."""
        smoothed = self.preprocess_image(image)
        thresh = cv2.adaptiveThreshold(smoothed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 13, 3)
        text = pytesseract.image_to_string(thresh)

        # Patterns to identify details
        pan_pattern = r'\b[A-Z]{5}\d{4}[A-Z]{1}\b'

        # Extracting details
        pan_match = re.search(pan_pattern, text)
        pan_number = pan_match.group(0) if pan_match else "Not Found"

        return {
            "pan_number": pan_number
        }

    def download_image(self, url):
        """Download an image from a URL."""
        response = requests.get(url)
        if response.status_code == 200:
            image = np.array(bytearray(response.content), dtype=np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            return image
        else:
            raise Exception("Failed to download image from URL.")
