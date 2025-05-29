import os

# Base paths
BASE_BACKEND = 'backend'
BASE_MODEL = os.path.join(BASE_BACKEND, 'model')
BASE_DATA = os.path.join(BASE_BACKEND, 'data')
BASE_TRAINING = os.path.join(BASE_BACKEND, 'training')

# Model files
MODEL_PATH = os.path.join(BASE_MODEL, 'sketch_model.keras')
BEST_MODEL_PATH = os.path.join(BASE_MODEL, 'best_sketch_model.keras')
CLASS_NAMES_PATH = os.path.join(BASE_MODEL, 'class_names.txt')

# Image used for testing predictions
SAMPLE_IMAGE_PATH = os.path.join(BASE_DATA, 'sample.png')
APPLE_IMAGE_PATH = os.path.join(BASE_DATA, 'apple.png')

# Quickdraw raw data location
QUICKDRAW_DATA_DIR = os.path.join(BASE_DATA, 'quickdraw_data')

# Training history
HISTORY_DIR = os.path.join(BASE_TRAINING, 'training_history')
PLOT_DIR = os.path.join(HISTORY_DIR, 'plots')
