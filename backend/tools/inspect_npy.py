import os
import numpy as np
import matplotlib.pyplot as plt
import random

# Absolute path from current script to the data directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'quickdraw_data')
SAVE_DIR = os.path.join(BASE_DIR, 'training', 'training_history', 'class_previews')
os.makedirs(SAVE_DIR, exist_ok=True)

classes = [f.replace(".npy", "") for f in os.listdir(DATA_DIR) if f.endswith(".npy")]

for cls in classes:
    path = os.path.join(DATA_DIR, f"{cls}.npy")
    data = np.load(path)
    print(f"{cls} → shape: {data.shape}")

    fig, axs = plt.subplots(1, 5, figsize=(10, 2))
    for ax in axs:
        idx = random.randint(0, len(data) - 1)
        ax.imshow(data[idx].reshape(28, 28), cmap="gray")
        ax.axis('off')
    plt.suptitle(f"Class: {cls}")
    plt.tight_layout()
    save_path = os.path.join(SAVE_DIR, f"{cls}_samples.png")
    plt.savefig(save_path)
    plt.close()
    print(f"✅ Saved preview: {save_path}")

