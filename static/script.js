// ----------------------------- 
// ClearMind Main Script 
// ----------------------------- 
 
const API_URL = "http://127.0.0.1:5000"; 
 
// ----------------------------- 
// Navigation Between Pages 
// ----------------------------- 
 
function showPage(pageId) {

    const pages = document.querySelectorAll(".page");
    const backBtn = document.getElementById("backBtn");

    pages.forEach(page => {
        page.style.display = "none";
    });

    const page = document.getElementById(pageId);
    if (page) {
        page.style.display = "block";
    }

    // Show 'back' arrow on any page except home
    if (backBtn) {
        backBtn.style.display = pageId === "homePage" ? "none" : "inline-flex";
    }
}
 
// Default page 
document.addEventListener("DOMContentLoaded", () => { 
    // Only run navigation if we're on the dashboard page (has homePage element)
    if (document.getElementById("homePage")) {
        showPage("homePage"); 
    }
}); 
 
 
// ----------------------------- 
// AI Topic Explanation 
// ----------------------------- 
 
 
async function explainTopic() {

    const topicInput = document.getElementById("topicInput");
    const responseBox = document.getElementById("explainResult");

    if (!topicInput || !responseBox) {
        console.error("Required HTML elements missing.");
        return;
    }

    const topic = topicInput.value.trim();

    if (!topic) {
        alert("Enter a topic first");
        return;
    }

    responseBox.innerHTML = "Generating explanation...";

    try {

        const res = await fetch(`${API_URL}/explain`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ topic: topic })
        });

        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }

        const data = await res.json();

        console.log("Response data:", data);

        if (data.status === "error") {
            responseBox.innerHTML = `Error: ${data.message}`;
            return;
        }

        responseBox.innerHTML =
            data.result ||
            data.explanation ||
            data.answer ||
            "No explanation returned.";

    } catch (error) {

        console.error(error);
        responseBox.innerHTML = "Error connecting to AI.";

    }
}

// -----------------------------
// Evaluate Student Explanation
// -----------------------------

async function evaluateExplanation() {

    const topicInput = document.getElementById("topicInput");
    const studentExplanation = document.getElementById("studentExplanation");
    const evaluationResult = document.getElementById("evaluationResult");

    if (!topicInput || !studentExplanation || !evaluationResult) {
        console.error("Required HTML elements missing.");
        return;
    }

    const topic = topicInput.value.trim();
    const explanation = studentExplanation.value.trim();

    if (!topic || !explanation) {
        alert("Enter both topic and your explanation first");
        return;
    }

    evaluationResult.innerHTML = "Evaluating explanation...";

    try {

        const res = await fetch(`${API_URL}/evaluate_explanation`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                topic: topic,
                explanation: explanation
            })
        });

        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }

        const data = await res.json();

        console.log("Response data:", data);

        if (data.status === "error") {
            evaluationResult.innerHTML = `Error: ${data.message}`;
            return;
        }

        evaluationResult.innerHTML = data.feedback;

    } catch (error) {

        console.error(error);
        evaluationResult.innerHTML = "Error connecting to AI.";

    }
}

// -----------------------------
// Analyze Reflection
// -----------------------------

async function analyzeReflection() {

    const reflectionText = document.getElementById("reflectionText");
    const reflectionAnalysis = document.getElementById("reflectionAnalysis");

    if (!reflectionText || !reflectionAnalysis) {
        console.error("Required HTML elements missing.");
        return;
    }

    const reflection = reflectionText.value.trim();

    if (!reflection) {
        alert("Write your reflection first");
        return;
    }

    reflectionAnalysis.innerHTML = "Analyzing reflection...";

    try {

        const res = await fetch(`${API_URL}/analyze_reflection`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                reflection: reflection
            })
        });

        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }

        const data = await res.json();

        console.log("Response data:", data);

        if (data.status === "error") {
            reflectionAnalysis.innerHTML = `Error: ${data.message}`;
            return;
        }

        reflectionAnalysis.innerHTML = data.analysis;

    } catch (error) {

        console.error(error);
        reflectionAnalysis.innerHTML = "Error connecting to AI.";

    }
}

// -----------------------------
// Calculate Mastery Score
// -----------------------------

async function calculateMastery() {

    const masteryScore = document.getElementById("masteryScore");

    if (!masteryScore) {
        console.error("Required HTML elements missing.");
        return;
    }

    // For now, use default scores or prompt user
    // In a real implementation, you might collect scores from previous interactions
    const explanationScore = 80; // Default or from previous evaluation
    const problemScore = 75;     // Default or from problem solving
    const revisionScore = 85;    // Default or from revision check
    const reflectionScore = 70;  // Default or from reflection analysis

    masteryScore.innerHTML = "Calculating mastery...";

    try {

        const res = await fetch(`${API_URL}/calculate_mastery`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                explanation: explanationScore,
                problem: problemScore,
                revision: revisionScore,
                reflection: reflectionScore
            })
        });

        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }

        const data = await res.json();

        console.log("Response data:", data);

        if (data.status === "error") {
            masteryScore.innerHTML = `Error: ${data.message}`;
            return;
        }

        masteryScore.innerHTML = `Your Mastery Score: ${data.mastery_score.toFixed(1)}%`;

    } catch (error) {

        console.error(error);
        masteryScore.innerHTML = "Error calculating mastery.";

    }
}

// -----------------------------
// Generate Real World Problems
// ----------------------------- 
 
async function generateProblem() { 
 
    const topicInput = document.getElementById("topicInput"); 
    const topic = topicInput ? topicInput.value : ""; 
    const level = "intermediate"; 
 
    const output = document.getElementById("problemOutput"); 
 
    output.innerHTML = "Generating problem..."; 
 
    try { 
 
        const res = await fetch(`${API_URL}/generate_problem`, { 
 
            method: "POST", 
            headers: { 
                "Content-Type": "application/json" 
            }, 
 
            body: JSON.stringify({ 
                topic: topic, 
                level: level 
            }) 
 
        }); 

        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }

        const data = await res.json(); 

        if (data.status === "error") {
            output.innerHTML = `Error: ${data.message}`;
            return;
        }

        output.innerHTML = data.problem; 
 
    } 
 
    catch(error) { 
 
        output.innerHTML = "Error generating problem."; 
 
    } 
 
} 
 
 
 
// ----------------------------- 
// Check Revision 
// ----------------------------- 
 
async function checkRevision() { 
 
    const topic = ""; 
    const revisionText = document.getElementById("revisionText").value; 
    const resultBox = document.getElementById("revisionFeedback"); 
 
    if (!revisionText) { 
        alert("Enter revision text first"); 
        return; 
    } 
 
    resultBox.innerHTML = "Analyzing revision..."; 
 
    try { 
 
        const res = await fetch(`${API_URL}/revision_check`, { 
 
            method: "POST", 
            headers: { 
                "Content-Type": "application/json" 
            }, 
            body: JSON.stringify({ 
                topic: topic, 
                revision: revisionText 
            }) 
 
        }); 
 
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }

        const data = await res.json(); 

        if (data.status === "error") {
            resultBox.innerHTML = `Error: ${data.message}`;
            return;
        }

        resultBox.innerHTML = data.revision_feedback; 
 
    } 
 
    catch(error) { 
 
        resultBox.innerHTML = "Error processing image."; 
 
    } 
 
} 
 
 
 
// ----------------------------- 
// Save Journaling Reflection 
// ----------------------------- 
 
function saveJournal() { 
 
    const date = document.getElementById("journalDate").value; 
    const text = document.getElementById("journalText").value; 
 
    if (!text) { 
        alert("Write something first"); 
        return; 
    } 
 
    let journals = JSON.parse(localStorage.getItem("journals")) || []; 
 
    journals.push({ 
        date: date, 
        text: text 
    }); 
 
    localStorage.setItem("journals", JSON.stringify(journals)); 
 
    alert("Journal saved!"); 
 
} 
 
 
 
// ----------------------------- 
// Save Mistake Reflection 
// ----------------------------- 
 
function saveMistake() { 
 
    const mistake = document.getElementById("mistakeType").value; 
    const reason = document.getElementById("mistakeReason").value; 
    const fix = document.getElementById("mistakeFix").value; 
 
    let mistakes = JSON.parse(localStorage.getItem("mistakes")) || []; 
 
    mistakes.push({ 
 
        mistake: mistake, 
        reason: reason, 
        fix: fix 
 
    }); 
 
    localStorage.setItem("mistakes", JSON.stringify(mistakes)); 
 
    alert("Mistake stored!"); 
 
} 
 
 
 
// ----------------------------- 
// Save Bias Reflection 
// ----------------------------- 
 
function saveBias() { 
 
    const bias = document.getElementById("biasName").value; 
    const solution = document.getElementById("biasSolution").value; 
    const improved = document.getElementById("biasImprove").value; 
 
    let biases = JSON.parse(localStorage.getItem("biases")) || []; 
 
    biases.push({ 
 
        bias: bias, 
        solution: solution, 
        improved: improved 
 
    }); 
 
    localStorage.setItem("biases", JSON.stringify(biases)); 
 
    alert("Bias saved!"); 
 
} 
 
 
 
// ----------------------------- 
// Planner Task System 
// ----------------------------- 
 
function addTask() { 
 
    const taskInput = document.getElementById("taskInput"); 
 
    const task = taskInput.value; 
 
    if (!task) { 
        alert("Enter a task"); 
        return; 
    } 
 
    const list = document.getElementById("taskList"); 
 
    const li = document.createElement("li"); 
 
    li.innerHTML = ` 
        <span>${task}</span> 
        <button onclick="completeTask(this)">Done</button> 
        <button onclick="deleteTask(this)">Delete</button> 
    `; 
 
    list.appendChild(li); 
 
    taskInput.value = ""; 
 
} 
 
 
 
function completeTask(button) { 
 
    const item = button.parentElement; 
 
    item.style.textDecoration = "line-through"; 
 
} 
 
 
 
function deleteTask(button) { 
 
    const item = button.parentElement; 
 
    item.remove(); 
 
} 
 
 
 
// ----------------------------- 
// Dark Mode Toggle 
// ----------------------------- 
 
function toggleDarkMode() { 
 
    document.body.classList.toggle("dark"); 
 
} 
 
 
 
// ----------------------------- 
// Smooth Scroll Animations 
// ----------------------------- 
 
window.addEventListener("scroll", () => { 
 
    const elements = document.querySelectorAll(".fade"); 
 
    elements.forEach(el => { 
 
        const position = el.getBoundingClientRect().top; 
 
        const screen = window.innerHeight; 
 
        if (position < screen - 100) { 
 
            el.classList.add("show"); 
 
        }
 
    }); 

});