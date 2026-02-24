import { updateStudentState } from '../services/state.js'
import { renderDashboard } from './dashboard.js'
import '../styles/dashboard.css'

let currentQuestionIndex = 0
let score = 0

const questions = [
  {
    question: "What is the expected value of a Binomial(n, p) distribution?",
    options: ["n + p", "n × p", "p / n", "n²p"],
    correct: "n × p"
  },
  {
    question: "What is the variance of a Binomial(n, p)?",
    options: ["np", "np(1 - p)", "n(1 - p)", "p(1 - n)"],
    correct: "np(1 - p)"
  }
]

export function renderQuiz() {
  const app = document.getElementById('app')
  app.innerHTML = `
    <div class="background-glow"></div>
    <div class="dashboard-container">
      <h1 class="dashboard-title">Adaptive Quiz</h1>
      <div class="card quiz-card" id="quizCard"></div>
    </div>
  `

  loadQuestion()
}

function loadQuestion() {
  const quizCard = document.getElementById('quizCard')
  const q = questions[currentQuestionIndex]

  quizCard.innerHTML = `
    <div class="question-text">${q.question}</div>
    <div class="options">
      ${q.options.map(opt => `<button class="option-btn">${opt}</button>`).join('')}
    </div>
    <button class="submit-btn" disabled>Submit Answer</button>
  `

  initializeInteractions(q)
}

function initializeInteractions(questionObj) {
  const options = document.querySelectorAll('.option-btn')
  const submitBtn = document.querySelector('.submit-btn')

  let selected = null

  options.forEach(btn => {
    btn.addEventListener('click', () => {
      options.forEach(b => b.classList.remove('selected'))
      btn.classList.add('selected')
      selected = btn.textContent
      submitBtn.disabled = false
    })
  })

  submitBtn.addEventListener('click', () => {
    evaluateAnswer(selected, questionObj.correct)
  })
}

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

  if (answer === correctAnswer) {
    score++
  }

  setTimeout(() => {
    goToNextQuestion()
  }, 1200)
}

function goToNextQuestion() {
  currentQuestionIndex++

  if (currentQuestionIndex >= questions.length) {
    showResults()
  } else {
    loadQuestion()
  }
}

function showResults() {
  const quizCard = document.getElementById('quizCard')

  const improvementFactor = score / questions.length

  // Simulated mastery update
  const newMastery = [
    80 + improvementFactor * 5,
    65 + improvementFactor * 5,
    72 + improvementFactor * 5,
    60 + improvementFactor * 5,
    75 + improvementFactor * 5
  ]

  // Simulated risk recalculation
  const newRisk = Math.max(10, 38 - improvementFactor * 20)

  // Update shared state
  updateStudentState({
    mastery: newMastery,
    risk: newRisk
  })

  // Render result screen
  quizCard.innerHTML = `
    <div class="question-text">Quiz Complete</div>
    <div style="margin-bottom:20px;">
      Your Score: ${score} / ${questions.length}
    </div>
    <button class="submit-btn" id="dashboardBtn">
      View Updated Dashboard
    </button>
  `

  // Attach click handler
  document.getElementById('dashboardBtn').addEventListener('click', () => {
    renderDashboard()
  })
}