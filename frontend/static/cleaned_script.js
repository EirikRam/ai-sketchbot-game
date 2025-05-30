// 🎨 Canvas Setup
const canvas = document.getElementById("sketchpad");
const ctx = canvas.getContext("2d");
let painting = false;

// let score = 0;
// // let currentPrompt = "";

let score = 0;
let strikes = 0;
const maxStrikes = 3;


// 🧮 Scoreboard UI Update
function updateScoreboard() {
    document.getElementById('scoreValue').textContent = score;
    document.getElementById('strikesValue').textContent = strikes;
}



// ✍️ Drawing Functions
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


// 🤖 AI Prediction Result Handling
function handlePredictionResult(prediction, actualPrompt) {
    const topGuess = prediction.toLowerCase();
    const correctAnswer = actualPrompt.toLowerCase();

    if (topGuess === correctAnswer) {
        score++;
        robotReact('happy');
        speak(`Yay! I guessed ${topGuess} correctly!`);
    } else {
        strikes++;
        robotReact('sad');
        speak(`Oops! I thought it was ${topGuess}.`);
    }

    updateScoreboard();

    if (strikes >= maxStrikes) {
        setTimeout(() => {
            endGame();
        }, 1000);
    } else {
        setTimeout(() => {
            startNewRound();
        }, 1500);
    }
}


// 🛑 Game Over & Reset Logic
function endGame() {
    const nickname = prompt("Game Over! You and the robot scored " + score + " points. Enter your nickname:");
    if (nickname) {
        saveScore(nickname, score);
    }
    resetGame();
}

function resetGame() {
    score = 0;
    strikes = 0;
    updateScoreboard();
    robotReact("idle");
    startNewRound();
}

function saveScore(name, value) {
    let scores = JSON.parse(localStorage.getItem("aiSketchbotScores") || "[]");
    scores.push({ name, value });
    localStorage.setItem("aiSketchbotScores", JSON.stringify(scores));
}


function newPrompt() {
    const random = Math.floor(Math.random() * classNames.length);
    currentPrompt = classNames[random];
    document.getElementById("draw-prompt").innerText = currentPrompt;
}


    document.getElementById("score").innerText = `Score: ${score} / ${attempts}`;
}

 else {
        robotImg.src = '/static/robot_sad.png';
        robotImg.style.transform = 'scale(0.9)';
    }

    // Revert to idle after 2 seconds
    setTimeout(() => {
        robotImg.src = '/static/robot_idle.png';
        robotImg.style.transform = 'scale(1)';
    }, 2000);
}

// Canvas mouse events

// 🖱️ Canvas Events
canvas.addEventListener("mousedown", startPosition);

// 🖱️ Canvas Events
canvas.addEventListener("mouseup", endPosition);

// 🖱️ Canvas Events
canvas.addEventListener("mousemove", draw);

// Clear canvas

// 🧹 Clear Button
document.getElementById("clearBtn").addEventListener("click", () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    document.getElementById("prediction").innerText = "";
});

// Predict button

// 🔍 Predict Drawing
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

// 🔄 Toggle Class List
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
