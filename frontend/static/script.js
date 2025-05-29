const canvas = document.getElementById("sketchpad");
const ctx = canvas.getContext("2d");
let painting = false;

let score = 0;
let attempts = 0;
let currentPrompt = "";

function startPosition(e) {
    painting = true;
    draw(e);
}

function endPosition() {
    painting = false;
    ctx.beginPath();
}

function draw(e) {
    if (!painting) return;

    ctx.lineWidth = 10;
    ctx.lineCap = "round";
    ctx.strokeStyle = "#000000";

    const rect = canvas.getBoundingClientRect();
    ctx.lineTo(e.clientX - rect.left, e.clientY - rect.top);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(e.clientX - rect.left, e.clientY - rect.top);
}

function newPrompt() {
    const random = Math.floor(Math.random() * classNames.length);
    currentPrompt = classNames[random];
    document.getElementById("draw-prompt").innerText = currentPrompt;
}

function updateScore(isCorrect) {
    attempts++;
    if (isCorrect) {
        score++;
        showCelebration();
    }
    document.getElementById("score").innerText = `Score: ${score} / ${attempts}`;
}

function updateRobotReaction(isCorrect) {
    const robotImg = document.getElementById('robot');
    if (isCorrect) {
        robotImg.src = '/static/robot_happy.png';
        robotImg.style.transform = 'scale(1.1)';
    } else {
        robotImg.src = '/static/robot_sad.png';
        robotImg.style.transform = 'scale(0.9)';
    }

    // Revert to idle after 2 seconds
    setTimeout(() => {
        robotImg.src = '/static/robot_idle.png';
        robotImg.style.transform = 'scale(1)';
    }, 2000);
}



function showCelebration() {
    const el = document.getElementById("celebration");
    el.classList.remove("hidden");
    setTimeout(() => el.classList.add("hidden"), 2000);  // Hide after 2s
}


// Canvas mouse events
canvas.addEventListener("mousedown", startPosition);
canvas.addEventListener("mouseup", endPosition);
canvas.addEventListener("mousemove", draw);

// Clear canvas
document.getElementById("clearBtn").addEventListener("click", () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    document.getElementById("prediction").innerText = "";
});

// Predict button
document.getElementById("predictBtn").addEventListener("click", async () => {
    const dataURL = canvas.toDataURL("image/png");
    const response = await fetch("/predict", {
        method: "POST",
        body: JSON.stringify({ image: dataURL }),
        headers: {
            "Content-Type": "application/json"
        }
    });

    const result = await response.json();
    const predicted = result.class || "unknown";
    document.getElementById("prediction").innerText = `Prediction: ${predicted}`;

    const predictedClass = result.class.toLowerCase();
    const isCorrect = predictedClass === currentPrompt.toLowerCase();

    updateScore(isCorrect);
    updateRobotReaction(isCorrect);  // ✅ Show robot reaction based on result
    newPrompt();  // Load next prompt
});

// Toggle class list
const toggleBtn = document.getElementById("toggle-classes-btn");
const classList = document.getElementById("class-list");

toggleBtn.addEventListener("click", () => {
    if (classList.classList.contains("hidden")) {
        classList.classList.remove("hidden");
        classList.innerHTML = classNames.map(name => `<li>${name}</li>`).join('');
        toggleBtn.textContent = "❌ Hide Classes";
    } else {
        classList.classList.add("hidden");
        toggleBtn.textContent = "🎨 What can I draw?";
    }
});

// Initialize game prompt
newPrompt();
