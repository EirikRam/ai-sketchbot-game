import tensorflow as tf
import numpy as np
from PIL import Image
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
MODEL_PATH = os.path.join(PROJECT_ROOT, 'backend', 'model', 'sketch_model_v3.keras')
CLASS_NAMES_PATH = os.path.join(PROJECT_ROOT, 'backend', 'model', 'class_names_v3.txt')
IMAGE_PATH = os.path.join(PROJECT_ROOT, 'backend', 'data', 'tree.jpg')

# Load model
model = tf.keras.models.load_model(MODEL_PATH)

# Load class names
with open(CLASS_NAMES_PATH, 'r') as f:
    CLASS_NAMES = [line.strip() for line in f.readlines()]

# Load and preprocess image
img = Image.open(IMAGE_PATH).convert('L').resize((28, 28))  # grayscale
img_array = np.array(img).reshape(1, 28, 28, 1) / 255.0

# Predict
pred = model.predict(img_array)
predicted_class = CLASS_NAMES[np.argmax(pred)]

print(f"Prediction: {predicted_class}")
