import {
  getStudentState,
  updateStudentState,
  updateCognitiveMastery,
  calculateRisk
} from '../services/state.js'

import '../styles/dashboard.css'
import { currentUser } from '../testApp.js'
import { renderStudentDashboard } from '../views/studentDashboardView.js'
import { mountView } from '../testApp.js'

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
  const state = getStudentState()

  conceptQueue = Object.keys(state.mastery)
  conceptStatus = {}

  conceptQueue.forEach(c => {
    conceptStatus[c] = false
  })

  mountView((container) => {
    container.innerHTML = `
      <div class="background-glow"></div>
      <div class="dashboard-container">
        <h1 class="dashboard-title">Diagnostic Quiz</h1>
        <div class="card quiz-card" id="quizCard"></div>
      </div>
    `
  })

  loadNextConcept()
}

/* ============================= */
/* LOAD NEXT CONCEPT */
/* ============================= */

function loadNextConcept() {
  const allDone = Object.values(conceptStatus).every(v => v === true)

  if (allDone) {
    showResults()
    return
  }

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
      ${question.options.map(opt =>
        `<button class="option-btn">${opt}</button>`
      ).join('')}
    </div>

    <div class="confidence-section">
      <p class="confidence-label">How confident are you?</p>
      <div class="confidence-options">
        <button class="confidence-btn" data-value="0.5">Guessing</button>
        <button class="confidence-btn" data-value="0.8">Somewhat Confident</button>
        <button class="confidence-btn" data-value="1.2">Very Confident</button>
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

  let selectedAnswer = null
  selectedConfidence = null

  function updateSubmitState() {
    submitBtn.disabled = !(selectedAnswer && selectedConfidence)
  }

  options.forEach(btn => {
    btn.addEventListener('click', () => {
      options.forEach(b => b.classList.remove('selected'))
      btn.classList.add('selected')
      selectedAnswer = btn.textContent
      updateSubmitState()
    })
  })

  confidenceButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      confidenceButtons.forEach(b => b.classList.remove('active'))
      btn.classList.add('active')
      selectedConfidence = parseFloat(btn.dataset.value)
      updateSubmitState()
    })
  })

  submitBtn.addEventListener('click', () => {
    if (!selectedAnswer || !selectedConfidence) return
    evaluateAnswer(selectedAnswer, questionObj.correct)
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

  const responseTime = (Date.now() - questionStartTime) / 1000
  const speedWeight = Math.max(0.5, 2 - responseTime / 5)
  const confidenceWeight =
    typeof selectedConfidence === 'number'
      ? selectedConfidence
      : 0.8

  const signalStrength = speedWeight * confidenceWeight

  updateCognitiveMastery(currentConcept, correct, signalStrength)
  conceptStatus[currentConcept] = true

  setTimeout(loadNextConcept, 900)
}

/* ============================= */
/* RESULTS */
/* ============================= */

function showResults() {
  const state = getStudentState()

  const recalculatedRisk = calculateRisk()

  updateStudentState({
    risk: recalculatedRisk
  })

  // Save updated state to session
  currentUser.hasTakenQuiz = true
  currentUser.data = getStudentState()

  // Directly render dashboard (acts as results screen)
  renderStudentDashboard(currentUser.data)
}