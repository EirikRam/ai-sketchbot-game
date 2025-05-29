import tensorflow as tf
import numpy as np
from PIL import Image
import os

MODEL_PATH = 'backend/model/sketch_model.keras'
CLASS_NAMES_PATH = 'backend/model/class_names.txt'
IMAGE_PATH = 'backend/data/apple.png'

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
