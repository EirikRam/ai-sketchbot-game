# AI Sketch-Bot – AI Drawing Classifier Game

![App Screenshot](frontend/assets/App%20Screenshot.png)

## 📘 Project Overview

**AI Sketch Bot** is a complete end-to-end AI-powered game built using a custom-trained image classification model that recognizes hand-drawn sketches in real time. This project encapsulates the full machine learning lifecycle: from dataset preparation and model training, to evaluation, GUI integration, and deployment via a modern web stack.

The project is a polished example of the **MLOps lifecycle in action**, where deep learning meets real-time inference through an interactive game.

---

## ⚙️ Technical Summary

- **Model**: Convolutional Neural Network (CNN) built and trained in TensorFlow/Keras using a curated dataset of 20 sketch categories.
- **Image Processing**: Drawings are collected from a browser `<canvas>` element, encoded as base64 PNGs, and preprocessed server-side using Pillow and NumPy.
- **Inference**: The image is resized, converted to grayscale, inverted (black background, white foreground), and normalized before prediction.
- **Frontend**: Built using HTML5, CSS3 (custom styling and animation), and vanilla JavaScript. All assets, including character illustrations and UI, are original.
- **Backend**: Python + Flask for routing and inference API.
- **Deployment**: Local development server using Flask. Designed to be hosted on any Python-compatible web server.

---

## 🧠 AI & Model Details

### Model Architecture

- Convolutional layers with ReLU activation
- MaxPooling for dimensionality reduction
- Flatten and Dense layers for classification
- Softmax output over 20 class categories

### Training & Evaluation

- Trained on a balanced dataset of sketch classes (e.g., moon, sun, cat, airplane, tree, etc.)
- Augmentation included basic transformations to enhance generalization
- Trained for multiple epochs with early stopping
- Evaluated using accuracy and loss metrics

![Model Accuracy](backend/training/training_history/plots/history_v3_20250529_2147_accuracy.png)
![Model Loss](backend/training/training_history/plots/history_v3_20250529_2147_loss.png)

---

## 🎮 Game Features

- **Live sketch canvas**: Users draw a sketch directly in the browser.
- **Top prediction**: The robot uses the trained model to guess the sketch.
- **Scoring system**: Tracks correct predictions and strikes.
- **Robot moods**: Visual feedback with custom robot artwork in three states:
  - Happy (`robot_happy.png`)
  - Sad (`robot_sad.png`)
  - Idle (`robot_idle.png`)

![Robot States](frontend/assets/Robot%20States.png)

- **Dynamic prompts**: Player is given random class prompts to draw.
- **Prediction UI**: Shows the AI’s guess and updates score or strikes.

---

## 💻 Technologies Used

| Category       | Tools/Technologies              |
|----------------|----------------------------------|
| Programming    | Python, JavaScript              |
| Frameworks     | TensorFlow, Flask               |
| Frontend       | HTML5, CSS3, Vanilla JS         |
| Image Handling | Pillow, NumPy                   |
| Plotting       | Matplotlib                      |
| Model Format   | `.keras` (SavedModel format)    |

---

## 📦 Project Structure

```
ai-sketchbot-game/
│
├── backend/
│   ├── api/
│   │   └── app.py
│   │
│   ├── data/
│   │   └── (your dataset files if any)
│   │
│   ├── inference/
│   │   ├── predict.py
│   │   └── test_prediction.py
│   │
│   ├── model/
│   │   ├── best_sketch_model.keras
│   │   ├── class_names.txt
│   │   ├── class_names_v2.txt
│   │   ├── class_names_v3.txt
│   │   ├── sketch_model.h5
│   │   ├── sketch_model.keras
│   │   ├── sketch_model_v2.keras
│   │   └── sketch_model_v3.keras
│   │
│   ├── tools/
│   │   ├── config.py
│   │   ├── gpu_test.py
│   │   └── inspect.npy.py
│   │
│   └── training/
│       ├── plot_training_history.py
│       ├── train_sketch_model.py
│       ├── train_sketch_model_v2.py
│       ├── train_sketch_model_v3.py
│       └── training_history/
│           └── evaluate.py
│
├── frontend/
│   ├── assets/
│   │   ├── App Screenshot.png
│   │   └── Robot States.png
│   │
│   ├── public/
│   │   └── index.html
│   │
│   └── static/
│       ├── class_names.js
│       ├── class_names_v2.txt
│       ├── robot_happy.png
│       ├── robot_idle.png
│       ├── robot_sad.png
│       ├── script.js
│       ├── style.css
│       └── target.jpg
│
├── README.md
├── requirements.txt
├── notes.txt
├── dir_structure.txt
└── .gitignore
```

---

## 🚀 How to Run

1. Clone this repository.
2. Make sure you have Python 3.9+ installed.
3. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Launch the Flask server:
   ```bash
   python app.py
   ```
5. Open your browser at `http://127.0.0.1:5000/`

---

## 🧩 Future Improvements

- Add model feedback and sketch labeling for user correction.
- Mobile responsiveness and touch drawing.
- Deploy on cloud (e.g., Render, Vercel with backend API).

---

## 👨‍💻 Created By

Eric Ramirez – AI Engineer & Full Stack Developer  
_All visual elements and logic are handcrafted._