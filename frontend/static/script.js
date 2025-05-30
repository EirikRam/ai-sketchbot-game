// ==============================
// 🎮 AI Sketchbot Game Script
// ==============================

// === Canvas Setup ===
const canvas = document.getElementById("sketchpad");
const ctx = canvas.getContext("2d");
let painting = false;
clearCanvas();

function clearCanvas() {
  ctx.fillStyle = "#FFFFFF";              // Set fill to white
  ctx.fillRect(0, 0, canvas.width, canvas.height);  // Fill entire canvas
  ctx.beginPath();                        // Reset the current drawing path
}

// === Game State ===
let currentPrompt = "";
let score = 0;
let strikes = 0;
const maxStrikes = 3;

// === Drawing Events ===
canvas.addEventListener("mousedown", startPosition);
canvas.addEventListener("mouseup", endPosition);
canvas.addEventListener("mousemove", draw);

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
  const rect = canvas.getBoundingClientRect();
  ctx.lineWidth = 10;
  ctx.lineCap = "round";
  ctx.strokeStyle = "#000000";
  ctx.lineTo(e.clientX - rect.left, e.clientY - rect.top);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(e.clientX - rect.left, e.clientY - rect.top);
}

// === 🔍 Debug: Confirm classNames loaded ===
console.log("classNames loaded:", Array.isArray(classNames), classNames?.length);


// === Prompt Logic ===
function newPrompt() {
  const randomIndex = Math.floor(Math.random() * classNames.length);
  currentPrompt = classNames[randomIndex];

  const promptEl = document.getElementById("prompt-text");
  const instructionsEl = document.getElementById("instructions");

  if (promptEl && instructionsEl) {
    //instructionsEl.classList.add("hidden"); // hide welcome message
    promptEl.classList.remove("hidden");    // show prompt
    promptEl.innerText = `🎯 Draw: ${currentPrompt}`;
  }
}


function getCanvasData() {
  return canvas.toDataURL("image/png");

}

// === Score/Strike UI ===
function updateScoreUI() {
  document.getElementById("scoreValue").innerText = score;
  document.getElementById("strikesValue").innerText = strikes;
}

// === Robot Mood / Feedback ===
/**
 * Updates the robot's facial expression and speech bubble.
 *
 * @param {string} mood - 'happy', 'sad', or 'idle'
 * @param {string} [message] - Optional custom message to show in the speech bubble
 */
function updateRobotMood(mood, message = "") {
    const robotSpeech = document.getElementById("robot-speech");
    const robotImage = document.getElementById("robot-image");

    let imageSrc, defaultMsg, animationClass;

    switch (mood) {
        case "happy":
            imageSrc = "/static/robot_happy.png";
            defaultMsg = "Yay! We got it right! 🎉";
            animationClass = "robot-bounce";
            break;
        case "sad":
            imageSrc = "/static/robot_sad.png";
            defaultMsg = "Oh no! I messed up... 😢";
            animationClass = "robot-shake";
            break;
        default:
            imageSrc = "/static/robot_idle.png";
            defaultMsg = "Let's draw something cool!";
            animationClass = "robot-float";
    }

    robotImage.src = imageSrc;
    robotSpeech.innerText = message || defaultMsg;

    // Remove existing animation classes
    robotImage.classList.remove("robot-bounce", "robot-shake", "robot-float");

    // Apply new animation
    void robotImage.offsetWidth; // Force reflow to retrigger animation
    robotImage.classList.add(animationClass);

    // Revert back to idle after 3s
    if (mood !== "idle") {
        setTimeout(() => {
            robotImage.src = "/static/robot_idle.png";
            robotSpeech.innerText = "Let's draw something cool!";
            robotImage.classList.remove("robot-bounce", "robot-shake");
            robotImage.classList.add("robot-float");
        }, 3000);
    }
}

// === Visual Effects ===
function showCelebration() {
  const el = document.getElementById("celebration");
  el.classList.remove("hidden");
  setTimeout(() => el.classList.add("hidden"), 2000);
}

// === Game Logic ===
function endGame() {
  alert(`Game Over! Final Score: ${score}`);
  const nickname = prompt("Enter your nickname:");
  if (nickname) {
    saveScore(nickname, score);
  }
  resetGame();
}

function resetGame() {
  score = 0;
  strikes = 0;
  currentPrompt = "";
  updateScoreUI();

  document.getElementById("prediction").innerText = "";

  const promptEl = document.getElementById("prompt-text");
  const instructionsEl = document.getElementById("instructions");

  if (promptEl && instructionsEl) {
    promptEl.classList.add("hidden");
    instructionsEl.classList.remove("hidden");
  }

  document.getElementById("robot-speech").innerText = "Let's draw something cool!";
}

function saveScore(name, value) {
  let scores = JSON.parse(localStorage.getItem("aiSketchbotScores") || "[]");
  scores.push({ name, value });
  localStorage.setItem("aiSketchbotScores", JSON.stringify(scores));
}

// === AI Prediction & Evaluation ===
document.getElementById("predictBtn").addEventListener("click", async () => {
  const imageData = getCanvasData(); // You should define this separately
  const response = await fetch("/predict", {
    method: "POST",
    body: JSON.stringify({ image: imageData }),
    headers: { "Content-Type": "application/json" }
  });

  const result = await response.json();
  const aiGuess = result.class;

  document.getElementById("prediction").innerText = `🤖 Robot guessed: ${aiGuess}`;

  if (aiGuess.toLowerCase() === currentPrompt.toLowerCase()) {
    score++;
    updateScoreUI();
    updateRobotMood("happy", `Yay! I guessed "${aiGuess}" right!`);
    showCelebration();
    nextPrompt();
  } else {
    strikes++;
    updateScoreUI();
    updateRobotMood("sad", `Oops! I thought it was "${aiGuess}"`);

    if (strikes >= maxStrikes) {
      endGame();
    }
  }
});

// === Canvas Clear ===
document.getElementById("clearBtn").addEventListener("click", () => {
  clearCanvas();  // Use the new function
  document.getElementById("prediction").innerText = "";
});


// === Start Challenge ===
document.getElementById("start-challenge-btn").addEventListener("click", () => {
  const instructions = document.getElementById("instructions");
  const promptText = document.getElementById("prompt-text");

  //if (instructions) instructions.classList.add("hidden");
  if (promptText) {
    promptText.classList.remove("hidden");
    const randomIndex = Math.floor(Math.random() * classNames.length);
    currentPrompt = classNames[randomIndex];
    promptText.innerText = `🎯 Draw: ${currentPrompt}`;
  }

  document.getElementById("robot-speech").innerText = "Draw it and let me guess!";
  clearCanvas();
  document.getElementById("prediction").innerText = "";
});

// === Toggle Class List ===
document.getElementById("toggle-classes-btn").addEventListener("click", () => {
  const classList = document.getElementById("class-list");
  const toggleBtn = document.getElementById("toggle-classes-btn");

  if (classList.classList.contains("hidden")) {
    classList.classList.remove("hidden");
    classList.innerHTML = classNames.map(name => `<li>${name}</li>`).join('');
    toggleBtn.textContent = "❌ Hide Classes";
  } else {
    classList.classList.add("hidden");
    toggleBtn.textContent = "🎨 What can I draw?";
  }
});

// === Initialize ===
// window.onload = () => {
//   newPrompt();
// };
