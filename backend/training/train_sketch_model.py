import os
import numpy as np
import urllib.request
import tensorflow as tf
import urllib.parse
import pickle
import json
from datetime import datetime
from sklearn.model_selection import train_test_split
from keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# from backend.config import (
#     MODEL_PATH, CLASS_NAMES_PATH, HISTORY_DIR
# )


# CONFIG
CLASS_NAMES = [
    'cat', 'dog', 'apple', 'car', 'tree', 'house', 'cup', 'bicycle', 'cloud', 'fish',
    'flower', 'star', 'face', 'moon', 'pizza',
    'light bulb', 'sun', 'airplane', 'candle', 'umbrella'
]
NUM_CLASSES = len(CLASS_NAMES)
EXAMPLES_PER_CLASS = 3000
TRAIN_RATIO = 0.9
BATCH_SIZE = 64
EPOCHS = 10

DATA_DIR = "../data/quickdraw_data"
URL_BASE = "https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/"

# Set seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

# Download & load data
def download_class_npy(class_name):
    raw_filename = f"{class_name}.npy"
    local_filename = raw_filename.replace(" ", "_")  # For local storage
    filepath = os.path.join(DATA_DIR, local_filename)
    if not os.path.exists(filepath):
        url = f"{URL_BASE}{urllib.parse.quote(raw_filename)}"
        print(f"Downloading {class_name}...")
        urllib.request.urlretrieve(url, filepath)
    return filepath

def load_data():
    os.makedirs(DATA_DIR, exist_ok=True)
    x_data, y_data = [], []

    for idx, class_name in enumerate(CLASS_NAMES):
        file_path = download_class_npy(class_name)
        data = np.load(file_path)
        data = data[:EXAMPLES_PER_CLASS]  # take only first N samples
        x_data.append(data)
        y_data.append(np.full(EXAMPLES_PER_CLASS, idx))

    x_data = np.vstack(x_data).reshape(-1, 28, 28, 1).astype('float32') / 255.0
    y_data = np.concatenate(y_data)
    y_data = tf.keras.utils.to_categorical(y_data, NUM_CLASSES)

    x_train, x_val, y_train, y_val = train_test_split(
        x_data, y_data, test_size=(1 - TRAIN_RATIO), stratify=y_data.argmax(axis=1), random_state=42
    )

    #ds_train = tf.data.Dataset.from_tensor_slices((x_train, y_train)).shuffle(10000).batch(BATCH_SIZE).prefetch(1)
    datagen = ImageDataGenerator(
        rotation_range=10,
        zoom_range=0.1,
        width_shift_range=0.1,
        height_shift_range=0.1
    )

    # This replaces the original ds_train
    ds_train = datagen.flow(x_train, y_train, batch_size=BATCH_SIZE)

    ds_val = tf.data.Dataset.from_tensor_slices((x_val, y_val)).batch(BATCH_SIZE).prefetch(1)

    return ds_train, ds_val, x_train

# Build model
def build_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(28, 28, 1)),
        tf.keras.layers.Conv2D(32, 3, activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(64, 3, activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(128, 3, activation='relu'),  # Extra Conv Layer
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(NUM_CLASSES, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model


# Train and save
if __name__ == "__main__":
    ds_train, ds_val, x_train = load_data()
    model = build_model()

    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=3,
        restore_best_weights=True,
        verbose=1
    )

    checkpoint = ModelCheckpoint(
        filepath='backend/model/best_sketch_model.keras',
        monitor='val_loss',
        save_best_only=True,
        verbose=1
    )

    history = model.fit(
        ds_train,
        epochs=EPOCHS,
        validation_data=ds_val,
        callbacks=[early_stopping, checkpoint]
    )

    # Save training training_history
    history_path = 'backend/training/training_history'
    os.makedirs(history_path, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    history_file = os.path.join(history_path, f'history_{timestamp}.json')

    with open(history_file, 'w') as f:
        json.dump(model.history.history, f)

    print(f"📈 Training training_history saved to {history_file}")

    model.save('backend/model/sketch_model.keras', save_format='keras_v3')

    with open('backend/model/class_names.txt', 'w') as f:
        for name in CLASS_NAMES:
            f.write(name + '\n')

    print("✅ Model training complete. Saved to backend/model/ as .keras and class_names.txt")
