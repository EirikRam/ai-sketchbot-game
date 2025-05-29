import base64
import io
import numpy as np
from PIL import Image
import tensorflow as tf
import os

# Compute path relative to project root, not script
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(PROJECT_ROOT, 'model', 'best_sketch_model.keras')
CLASS_NAMES_PATH = os.path.join(PROJECT_ROOT, 'model', 'class_names.txt')

# Load model and class names
model = tf.keras.models.load_model(MODEL_PATH)

with open(CLASS_NAMES_PATH, 'r') as f:
    CLASS_NAMES = [line.strip() for line in f.readlines()]

def preprocess_image(image_data):
    image_bytes = base64.b64decode(image_data.split(',')[1])
    image = Image.open(io.BytesIO(image_bytes)).convert('L').resize((28, 28))
    image_array = np.array(image).reshape(1, 28, 28, 1) / 255.0
    return image_array

def predict(image_data):
    input_array = preprocess_image(image_data)
    predictions = model.predict(input_array)
    top_index = np.argmax(predictions)
    top_class = CLASS_NAMES[top_index]
    confidence = float(np.max(predictions))
    return {'class': top_class, 'confidence': round(confidence * 100, 2)}
