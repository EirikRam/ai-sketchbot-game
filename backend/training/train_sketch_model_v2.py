import os
import numpy as np
import urllib.request
import tensorflow as tf
import urllib.parse
import json
from datetime import datetime
from sklearn.model_selection import train_test_split
from keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# ==== CONFIGURATION ====
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
MODEL_SAVE_NAME = "sketch_model_v2.keras"
CLASS_FILE_NAME = "class_names_v2.txt"
HISTORY_DIR = "backend/training/training_history"

URL_BASE = "https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/"

np.random.seed(42)
tf.random.set_seed(42)

# ==== DOWNLOAD AND LOAD DATA ====
def download_class_npy(class_name):
    raw_filename = f"{class_name}.npy"
    local_filename = raw_filename.replace(" ", "_")
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
        data = 255 - data  # Invert image: white-on-black
        data = data[:EXAMPLES_PER_CLASS]
        x_data.append(data)
        y_data.append(np.full(EXAMPLES_PER_CLASS, idx))

    x_data = np.vstack(x_data).reshape(-1, 28, 28, 1).astype('float32') / 255.0
    y_data = np.concatenate(y_data)
    y_data = tf.keras.utils.to_categorical(y_data, NUM_CLASSES)

    x_train, x_val, y_train, y_val = train_test_split(
        x_data, y_data, test_size=(1 - TRAIN_RATIO), stratify=y_data.argmax(axis=1), random_state=42
    )

    datagen = ImageDataGenerator(
        rotation_range=15,
        zoom_range=0.2,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=10,
        brightness_range=(0.7, 1.3)
    )
    ds_train = datagen.flow(x_train, y_train, batch_size=BATCH_SIZE)
    ds_val = tf.data.Dataset.from_tensor_slices((x_val, y_val)).batch(BATCH_SIZE).prefetch(1)

    return ds_train, ds_val

# ==== MODEL DEFINITION ====
def build_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(28, 28, 1)),
        tf.keras.layers.Conv2D(64, 3, padding='same', activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(),

        tf.keras.layers.Conv2D(128, 3, padding='same', activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(),

        tf.keras.layers.Conv2D(256, 3, padding='same', activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Flatten(),

        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(NUM_CLASSES, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# ==== TRAIN & SAVE ====
if __name__ == "__main__":
    ds_train, ds_val = load_data()
    model = build_model()

    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    model_path = f"backend/model/{MODEL_SAVE_NAME}"
    class_file_path = f"backend/model/{CLASS_FILE_NAME}"
    history_file_path = os.path.join(HISTORY_DIR, f"history_v2_{timestamp}.json")

    os.makedirs("backend/model", exist_ok=True)
    os.makedirs(HISTORY_DIR, exist_ok=True)

    early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True, verbose=1)
    checkpoint = ModelCheckpoint(filepath=model_path, monitor='val_loss', save_best_only=True, verbose=1)

    history = model.fit(
        ds_train,
        epochs=EPOCHS,
        validation_data=ds_val,
        callbacks=[early_stopping, checkpoint]
    )

    with open(history_file_path, 'w') as f:
        json.dump(history.history, f)

    with open(class_file_path, 'w') as f:
        for name in CLASS_NAMES:
            f.write(name + '\n')

    print(f"✅ New model saved: {model_path}")
    print(f"📈 Training history saved: {history_file_path}")
