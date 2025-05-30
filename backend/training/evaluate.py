import os
import json
import matplotlib.pyplot as plt

HISTORY_DIR = 'backend/training/training_history'
PLOT_DIR = os.path.join(HISTORY_DIR, 'plots')
os.makedirs(PLOT_DIR, exist_ok=True)

def load_histories():
    histories = {}
    print("Files in directory:", os.listdir(HISTORY_DIR))  # 🔍 ADD THIS LINE
    for file in os.listdir(HISTORY_DIR):
        if file.endswith('.json'):
            path = os.path.join(HISTORY_DIR, file)
            with open(path, 'r') as f:
                data = json.load(f)
                histories[file] = data
    return histories

def plot_history(histories):
    for filename, history in histories.items():
        name = filename.replace('.json', '')

        # Plot accuracy
        plt.figure()
        plt.plot(history['accuracy'], label='Train Accuracy')
        plt.plot(history['val_accuracy'], label='Val Accuracy')
        plt.title(f'Accuracy - {name}')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(PLOT_DIR, f'{name}_accuracy.png'))
        plt.close()

        # Plot loss
        plt.figure()
        plt.plot(history['loss'], label='Train Loss')
        plt.plot(history['val_loss'], label='Val Loss')
        plt.title(f'Loss - {name}')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(PLOT_DIR, f'{name}_loss.png'))
        plt.close()

        print(f"Plots saved for {name}")

if __name__ == '__main__':
    histories = load_histories()
    if not histories:
        print("No training histories found.")
    else:
        plot_history(histories)
        print("Histories loaded:", histories.keys())
        # Plot combined val_accuracy for all runs
        plt.figure()
        for filename, history in histories.items():
            name = filename.replace('.json', '')
            plt.plot(history['val_accuracy'], label=name)

        plt.title('📈 Validation Accuracy Comparison')
        plt.xlabel('Epoch')
        plt.ylabel('Val Accuracy')
        plt.legend(fontsize='small', loc='lower right')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(PLOT_DIR, 'val_accuracy_comparison.png'))
        plt.close()
        print("Combined val_accuracy comparison plot saved.")

