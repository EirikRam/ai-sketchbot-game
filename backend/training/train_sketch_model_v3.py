import os
import datetime
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers, models
import json
from sklearn.model_selection import train_test_split

# === Paths ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data", "quickdraw_data")
MODEL_DIR = os.path.join(SCRIPT_DIR, "..", "model")
HISTORY_DIR = os.path.join(SCRIPT_DIR, "..", "training", "training_history")
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(HISTORY_DIR, exist_ok=True)

# === Versioning ===
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
model_filename = f"sketch_model_v3_{timestamp}.keras"
history_filename = f"history_v3_{timestamp}.json"

# === Load .npy class files ===
CLASS_NAMES = sorted([f.replace(".npy", "") for f in os.listdir(DATA_DIR) if f.endswith(".npy")])
x_data = []
y_data = []

for idx, class_name in enumerate(CLASS_NAMES):
    path = os.path.join(DATA_DIR, f"{class_name}.npy")
    if os.path.exists(path):
        data = np.load(path)
        data = 255 - data  # invert black-on-white
        data = data[:3000]  # limit per class
        x_data.append(data)
        y_data.append(np.full(data.shape[0], idx))

x_data = np.vstack(x_data).reshape(-1, 28, 28, 1).astype("float32") / 255.0
y_data = np.concatenate(y_data)

# === Split ===
x_train, x_val, y_train, y_val = train_test_split(x_data, y_data, test_size=0.2, stratify=y_data, random_state=42)

# === Model ===
model = models.Sequential([
    layers.Input(shape=(28, 28, 1)),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(len(CLASS_NAMES), activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# === Train ===
history = model.fit(
    x_train, y_train,
    validation_data=(x_val, y_val),
    epochs=10,
    batch_size=64,
    callbacks=[
        keras.callbacks.ModelCheckpoint(os.path.join(MODEL_DIR, model_filename), save_best_only=True, monitor='val_loss'),
        keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True)
    ]
)

# === Save History ===
with open(os.path.join(HISTORY_DIR, history_filename), 'w') as f:
    json.dump(history.history, f)

# === Save class names ===
with open(os.path.join(MODEL_DIR, f"class_names_v3_{timestamp}.txt"), 'w') as f:
    f.write("\n".join(CLASS_NAMES))

print(f"✅ Model saved to: {model_filename}")
print(f"📈 History saved to: {history_filename}")
