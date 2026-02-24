import {
  getStudentState,
  updateStudentState,
  updateCognitiveMastery
} from '../services/state.js'
import { renderDashboard } from './dashboard.js'
import '../styles/dashboard.css'

/* ============================= */
/* DIAGNOSTIC TRACKING */
/* ============================= */

let conceptQueue = []
let conceptStatus = {}
let currentConcept = null
let questionStartTime = null
let selectedConfidence = null

/* ============================= */
/* QUESTION BANK */
/* ============================= */

const questionBank = {
  Binomial: [
    {
      question: "What is E[X] for Binomial(n,p)?",
      options: ["n + p", "n × p", "p / n", "n²p"],
      correct: "n × p"
    }
  ],
  Poisson: [
    {
      question: "Variance of Poisson(λ)?",
      options: ["λ", "λ²", "√λ", "λ+1"],
      correct: "λ"
    }
  ],
  Normal: [
    {
      question: "Mean of Normal(μ, σ²)?",
      options: ["μ", "σ", "μ²", "σ²"],
      correct: "μ"
    }
  ],
  Bayes: [
    {
      question: "Bayes theorem updates what?",
      options: ["Likelihood", "Prior", "Posterior", "Variance"],
      correct: "Posterior"
    }
  ],
  Conditional: [
    {
      question: "P(A|B) means?",
      options: [
        "Probability of A",
        "Probability of B",
        "Probability of A given B",
        "Joint probability"
      ],
      correct: "Probability of A given B"
    }
  ]
}

/* ============================= */
/* RENDER QUIZ */
/* ============================= */

export function renderQuiz() {
  const app = document.getElementById('app')

  const state = getStudentState()

  conceptQueue = Object.keys(state.mastery)
  conceptStatus = {}

  conceptQueue.forEach(c => {
    conceptStatus[c] = false
  })

  app.innerHTML = `
    <div class="background-glow"></div>
    <div class="dashboard-container">
      <h1 class="dashboard-title">Diagnostic Quiz</h1>
      <div class="card quiz-card" id="quizCard"></div>
    </div>
  `

  loadNextConcept()
}

/* ============================= */
/* LOAD NEXT CONCEPT */
/* ============================= */

function loadNextConcept() {
  // If all concepts mastered at least once → finish
  const allDone = Object.values(conceptStatus).every(v => v === true)

  if (allDone) {
    showResults()
    return
  }

  // Pick next unfinished concept
  currentConcept = conceptQueue.find(c => conceptStatus[c] !== true)

  loadQuestionForConcept(currentConcept)
}

function loadQuestionForConcept(concept) {
  const quizCard = document.getElementById('quizCard')
  const question = questionBank[concept][0]
  questionStartTime = Date.now()

  quizCard.innerHTML = `
  <div class="question-text">${question.question}</div>

  <div class="options">
    ${question.options.map(opt => `<button class="option-btn">${opt}</button>`).join('')}
  </div>

  <div class="confidence-section">
  <p class="confidence-label">How confident are you?</p>

  <div class="confidence-options">
    <button class="confidence-btn" data-value="0.5">
      Guessing
    </button>

    <button class="confidence-btn" data-value="0.8">
      Somewhat Confident
    </button>

    <button class="confidence-btn" data-value="1.2">
      Very Confident
    </button>
  </div>
</div>

  <button class="submit-btn" disabled>Submit Answer</button>
`

  initializeInteractions(question)
}

/* ============================= */
/* INTERACTIONS */
/* ============================= */

function initializeInteractions(questionObj) {
  const options = document.querySelectorAll('.option-btn')
  const submitBtn = document.querySelector('.submit-btn')
  const confidenceButtons = document.querySelectorAll('.confidence-btn')

  let selected = null
  selectedConfidence = null

  options.forEach(btn => {
    btn.addEventListener('click', () => {
      options.forEach(b => b.classList.remove('selected'))
      btn.classList.add('selected')
      selected = btn.textContent
      submitBtn.disabled = false
    })
  })

  confidenceButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      confidenceButtons.forEach(b => b.classList.remove('active'))
      btn.classList.add('active')
      selectedConfidence = parseFloat(btn.dataset.value)
    })
  })

  submitBtn.addEventListener('click', () => {
    evaluateAnswer(selected, questionObj.correct)
  })
}

/* ============================= */
/* EVALUATE */
/* ============================= */

function evaluateAnswer(answer, correctAnswer) {
  const options = document.querySelectorAll('.option-btn')

  options.forEach(btn => {
    if (btn.textContent === correctAnswer) {
      btn.classList.add('correct')
    }
    if (btn.textContent === answer && answer !== correctAnswer) {
      btn.classList.add('incorrect')
    }
    btn.disabled = true
  })

  const correct = answer === correctAnswer

  // Calculate response time in seconds
  const responseTime = (Date.now() - questionStartTime) / 1000

  // Speed weight (faster = higher)
  const speedWeight = Math.max(0.5, 2 - responseTime / 5)

  // Confidence weight (default medium if none selected)
  const confidenceWeight =
  typeof selectedConfidence === 'number'
    ? selectedConfidence
    : 0.8

  // Final signal strength
  const signalStrength = speedWeight * confidenceWeight

  updateCognitiveMastery(currentConcept, correct, signalStrength)

  conceptStatus[currentConcept] = true

  setTimeout(() => {
    loadNextConcept()
  }, 900)
}

/* ============================= */
/* RESULTS */
/* ============================= */

function showResults() {
  const quizCard = document.getElementById('quizCard')
  const state = getStudentState()

  // Extract mastery values
  const masteryValues = Object.values(state.mastery)

  // Compute average mastery (for display only)
  const averageMastery =
    masteryValues.reduce((sum, val) => sum + val, 0) / masteryValues.length

  // Determine weakest concept
  const weakestEntry = Object.entries(state.mastery)
    .sort((a, b) => a[1] - b[1])[0]

  const weakestConcept = weakestEntry[0]
  const weakestScore = weakestEntry[1]

  // Risk is based on weakest concept (diagnostic model)
  const recalculatedRisk = Math.max(5, 100 - weakestScore)

  // Update global state
  updateStudentState({
    risk: recalculatedRisk
  })

  quizCard.innerHTML = `
    <div class="question-text">Diagnostic Complete</div>
    <div style="margin-bottom:10px;">
      Average Mastery: ${Math.round(averageMastery)}%
    </div>
    <div style="margin-bottom:20px;">
      Weakest Concept: <strong>${weakestConcept}</strong>
    </div>
    <button class="submit-btn" id="dashboardBtn">
      View Updated Dashboard
    </button>
  `

  document.getElementById('dashboardBtn').addEventListener('click', () => {
    renderDashboard()
  })
}