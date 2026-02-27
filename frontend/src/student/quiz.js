let attemptLog = []
let activeTestId = null
let isCustomTest = false
let customQuestionIndex = 0
let customQuestions = []

import { renderTestBreakdown } from '../views/studentHomeView.js'

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
import { saveTestAttempt } from '../services/classroomStore.js'

/* ============================= */
/* DIAGNOSTIC TRACKING */
/* ============================= */

let conceptQueue = []
let conceptStatus = {}
let currentConcept = null
let questionStartTime = null
let selectedConfidence = null
let selectedAnswers = new Set()

/* ============================= */
/* QUESTION BANK */
/* ============================= */

const questionBank = {
  Binomial: [
    {
      question: "What is E[X] for Binomial(n,p)?",
      options: ["n + p", "n × p", "p / n", "n²p"],
      correct: ["n × p"],
      multi: false
    },
    {
      question: "Which are properties of a Binomial distribution?",
      options: [
        "Fixed number of trials",
        "Independent trials",
        "Continuous outcomes",
        "Two possible outcomes per trial",
        "Constant probability of success",
        "Events occur randomly in time"
      ],
      correct: [
        "Fixed number of trials",
        "Independent trials",
        "Two possible outcomes per trial",
        "Constant probability of success"
      ],
      multi: true
    }
  ],

  Poisson: [
    {
      question: "Variance of Poisson(λ)?",
      options: ["λ", "λ²", "√λ", "λ+1"],
      correct: ["λ"],
      multi: false
    },
    {
      question: "Which statements are true about a Poisson distribution?",
      options: [
        "Used for rare events",
        "Defined for discrete counts",
        "Mean equals variance",
        "Requires fixed number of trials",
        "Events are independent",
        "It is continuous"
      ],
      correct: [
        "Used for rare events",
        "Defined for discrete counts",
        "Mean equals variance",
        "Events are independent"
      ],
      multi: true
    }
  ],

  Normal: [
    {
      question: "Mean of Normal(μ, σ²)?",
      options: ["μ", "σ", "μ²", "σ²"],
      correct: ["μ"],
      multi: false
    },
    {
      question: "Which are properties of a Normal distribution?",
      options: [
        "Symmetric about mean",
        "Continuous",
        "Defined by μ and σ²",
        "Area under curve = 1",
        "Discrete",
        "Skewed right",
        "Bell-shaped"
      ],
      correct: [
        "Symmetric about mean",
        "Continuous",
        "Defined by μ and σ²",
        "Area under curve = 1",
        "Bell-shaped"
      ],
      multi: true
    }
  ],

  Bayes: [
    {
      question: "Bayes theorem updates what?",
      options: ["Likelihood", "Prior", "Posterior", "Variance"],
      correct: ["Posterior"],
      multi: false
    },
    {
      question: "Which quantities appear in Bayes' Theorem?",
      options: [
        "Prior probability",
        "Likelihood",
        "Posterior probability",
        "Marginal probability",
        "Variance",
        "Standard deviation"
      ],
      correct: [
        "Prior probability",
        "Likelihood",
        "Posterior probability",
        "Marginal probability"
      ],
      multi: true
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
      correct: ["Probability of A given B"],
      multi: false
    },
    {
      question: "Which statements are true about conditional probability?",
      options: [
        "P(A|B) = P(A ∩ B) / P(B)",
        "Requires P(B) ≠ 0",
        "Always equals P(A)",
        "Depends on given event",
        "Symmetric in A and B",
        "Can change when new evidence arrives"
      ],
      correct: [
        "P(A|B) = P(A ∩ B) / P(B)",
        "Requires P(B) ≠ 0",
        "Depends on given event",
        "Can change when new evidence arrives"
      ],
      multi: true
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
  const questions = questionBank[concept]
  const question =
    questions[Math.floor(Math.random() * questions.length)]

  loadQuestionUI(question)
}

/* ============================= */
/* INTERACTIONS */
/* ============================= */

function initializeInteractions(questionObj) {
  const options = document.querySelectorAll('.option-btn')
  const submitBtn = document.querySelector('.submit-btn')
  const confidenceButtons = document.querySelectorAll('.confidence-btn')

  function updateSubmitState() {
    submitBtn.disabled =
      !(selectedAnswers.size > 0 && selectedConfidence)
  }

  options.forEach(btn => {
    btn.addEventListener('click', () => {
      const value = btn.dataset.value

      if (questionObj.multi) {
        // Toggle selection
        if (selectedAnswers.has(value)) {
          selectedAnswers.delete(value)
          btn.classList.remove('selected')
        } else {
          selectedAnswers.add(value)
          btn.classList.add('selected')
        }
      } else {
        // Single select
        selectedAnswers.clear()
        options.forEach(b => b.classList.remove('selected'))
        selectedAnswers.add(value)
        btn.classList.add('selected')
      }

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
    evaluateAnswer(questionObj)
  })
}

/* ============================= */
/* EVALUATE */
/* ============================= */

function evaluateAnswer(questionObj) {

  const options = document.querySelectorAll('.option-btn')
  const correctSet = new Set(questionObj.correct)

  const fullyCorrect =
    selectedAnswers.size === correctSet.size &&
    [...selectedAnswers].every(ans => correctSet.has(ans))

  options.forEach(btn => {
    const value = btn.dataset.value

    if (correctSet.has(value)) {
      btn.classList.add('correct')
    }

    if (
      selectedAnswers.has(value) &&
      !correctSet.has(value)
    ) {
      btn.classList.add('incorrect')
    }

    btn.disabled = true
  })

  const responseTime = (Date.now() - questionStartTime) / 1000
  const speedWeight = Math.max(0.5, 2 - responseTime / 5)
  const confidenceWeight =
    typeof selectedConfidence === 'number'
      ? selectedConfidence
      : 0.8

  const signalStrength = speedWeight * confidenceWeight

  /* ============================= */
  /* CUSTOM TEST MODE */
  /* ============================= */

  if (isCustomTest) {

    attemptLog.push({
      question: questionObj.question,
      selected: [...selectedAnswers],
      correct: questionObj.correct,
      wasCorrect: fullyCorrect
    })

    setTimeout(() => {
      loadCustomQuestion()
    }, 800)

    return
  }

  /* ============================= */
  /* DIAGNOSTIC MODE */
  /* ============================= */

  updateCognitiveMastery(
    currentConcept,
    fullyCorrect,
    signalStrength
  )

  conceptStatus[currentConcept] = true

  setTimeout(loadNextConcept, 800)
}

/* ============================= */
/* RESULTS */
/* ============================= */

function showResults() {

  const recalculatedRisk = calculateRisk()

  updateStudentState({
    risk: recalculatedRisk
  })

  /* ============================= */
  /* CUSTOM TEST FLOW */
  /* ============================= */

  if (isCustomTest) {

    if (!currentUser.completedTests) {
      currentUser.completedTests = []
    }

    const attemptData = {
      testId: activeTestId,
      topic: currentConcept,
      questions: attemptLog,
      score: attemptLog.filter(q => q.wasCorrect).length,
      total: attemptLog.length,
      timestamp: Date.now()
    }

    /* Save inside student session */
    currentUser.completedTests.push(attemptData)

    /* 🔥 Save inside classroom (teacher access) */
    if (currentUser.activeClass) {
      saveTestAttempt(
        currentUser.activeClass,
        currentUser.id,
        attemptData
      )
    }

    /* 🔥 Update dashboard data */
    currentUser.data = getStudentState()

    /* Show breakdown immediately */
    renderTestBreakdown(activeTestId)

    /* Reset custom mode */
    isCustomTest = false
    attemptLog = []
    activeTestId = null

    return
  }

  /* ============================= */
  /* DIAGNOSTIC FLOW */
  /* ============================= */

  currentUser.hasTakenQuiz = true
  currentUser.data = getStudentState()

  renderStudentDashboard(currentUser.data)
}


export function renderCustomTest(test) {

  isCustomTest = true
  activeTestId = test.id
  attemptLog = []
  customQuestionIndex = 0
  currentConcept = test.topic

  const pool = questionBank[test.topic]

  // 🔥 Build fixed question list once
  customQuestions = []

  for (let i = 0; i < test.numQuestions; i++) {
    const random =
      pool[Math.floor(Math.random() * pool.length)]
    customQuestions.push(random)
  }

  mountView((container) => {
    container.innerHTML = `
      <div class="dashboard-container">
        <h1>${test.topic} Test</h1>
        <div class="card quiz-card" id="quizCard"></div>
      </div>
    `
  })

  loadCustomQuestion()
}

function loadCustomQuestion() {

  if (customQuestionIndex >= customQuestions.length) {
    showResults()
    return
  }

  const question =
    customQuestions[customQuestionIndex]

  loadQuestionUI(question)

  customQuestionIndex++
}

function loadQuestionUI(question) {
  const quizCard = document.getElementById('quizCard')

  questionStartTime = Date.now()
  selectedAnswers = new Set()
  selectedConfidence = null

  quizCard.innerHTML = `
    <div class="question-text">${question.question}</div>

    ${question.multi ? `
      <div class="multi-hint">
        Select all that apply.
      </div>
    ` : ''}

    <div class="options">
      ${question.options.map(opt => `
        <button class="option-btn" data-value="${opt}">
          ${opt}
        </button>
      `).join('')}
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