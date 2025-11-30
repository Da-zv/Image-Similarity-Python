# image_processing.py

import cv2
import imagehash
from PIL import Image

def load_image(path):
    image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Could not load image: {path}")
    image = cv2.resize(image, (256, 256), interpolation=cv2.INTER_LINEAR)
    return image

def calculate_histogram(image):
    image = cv2.Canny(image, 50, 150)
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    return hist

def calculate_phash(image_path):
    image = Image.open(image_path)
    phash = imagehash.phash(image)
    return phash
