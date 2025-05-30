import base64
import io
import numpy as np
from PIL import Image, ImageOps
import tensorflow as tf
import os

# Compute path relative to project root, not script
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(PROJECT_ROOT, 'model', 'sketch_model_v3.keras')
CLASS_NAMES_PATH = os.path.join(PROJECT_ROOT, 'model', 'class_names_v3.txt')

# Load model and class names
model = tf.keras.models.load_model(MODEL_PATH)

with open(CLASS_NAMES_PATH, 'r') as f:
    CLASS_NAMES = [line.strip() for line in f.readlines()]

# # Debug version
# def preprocess_image(image_data):
#     import uuid
#     import matplotlib.pyplot as plt
#
#     # Decode the base64 PNG
#     image_bytes = base64.b64decode(image_data.split(',')[1])
#     image = Image.open(io.BytesIO(image_bytes))
#
#     # Resize before converting to grayscale
#     image = image.resize((28, 28))            # Resize while still RGBA/Color
#     image = image.convert('L')                # Then convert to grayscale
#     image = ImageOps.invert(image)            # Invert to match training data (white on black)
#
#     # Save debug image (optional)
#     debug_filename = f"debug_{uuid.uuid4().hex[:6]}.png"
#     image.save(debug_filename)
#     print(f"[DEBUG] Saved input preview: {debug_filename}")
#
#     # Plot preview (optional)
#     plt.imshow(image, cmap='gray')
#     plt.title("Processed Model Input")
#     plt.show()
#
#     # Prepare as NumPy input for model
#     image_array = np.array(image).reshape(1, 28, 28, 1) / 255.0
#     return image_array

def preprocess_image(image_data):
    """Convert base64 image data to a normalized NumPy array suitable for prediction."""
    image_bytes = base64.b64decode(image_data.split(',')[1])
    image = Image.open(io.BytesIO(image_bytes))
    image = image.resize((28, 28))
    image = image.convert('L')
    image = ImageOps.invert(image)
    image_array = np.array(image).reshape(1, 28, 28, 1) / 255.0
    return image_array

def predict(image_data):
    input_array = preprocess_image(image_data)

    # 🔍 Add debug visualization
    import matplotlib.pyplot as plt
    plt.imshow(input_array[0, :, :, 0], cmap='gray')
    plt.title("Model Input Preview")
    plt.show()

    predictions = model.predict(input_array)
    top_index = np.argmax(predictions)
    top_class = CLASS_NAMES[top_index]
    confidence = float(np.max(predictions))
    return {'class': top_class, 'confidence': round(confidence * 100, 2)}
