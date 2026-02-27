let attemptLog = []
let activeTestId = null
let isCustomTest = false
let customQuestionIndex = 0
let customQuestions = []
let questionsByConcept = {}  // Loaded from API

import { renderTestBreakdown } from '../views/studentHomeView.js'
import { getStudentState, updateStudentState, updateCognitiveMastery, calculateRisk } from '../services/state.js'
import { fetchAllQuestions, fetchQuestionsByConcept, checkHasAttemptedQuiz } from '../services/api.js'
import '../styles/dashboard.css'
import { currentUser } from '../testApp.js'
import { renderStudentDashboard } from '../views/studentDashboardView.js'
import { mountView } from '../testApp.js'
import { saveTestAttempt } from '../services/classroomStore.js'

let conceptQueue = []
let conceptStatus = {}
let currentConcept = null
let questionStartTime = null
let selectedConfidence = null
let selectedAnswers = new Set()

export async function renderQuiz() {
  try {
    const quizStatus = await checkHasAttemptedQuiz()
    if (quizStatus.has_attempted) {
      alert("You have already taken the diagnostic quiz. You cannot re-attempt it.")
      return
    }
    
    const state = getStudentState()
    conceptQueue = Object.keys(state.mastery)
    conceptStatus = {}
    conceptQueue.forEach(c => {
      conceptStatus[c] = false
    })

    questionsByConcept = await fetchAllQuestions()

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
  } catch (error) {
    console.error("Failed to load quiz:", error)
    alert("Failed to load quiz. Please try again.")
  }
}

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
  const questions = questionsByConcept[concept]
  
  if (!questions || questions.length === 0) {
    console.error(`No questions found for concept: ${concept}`)
    loadNextConcept()
    return
  }
  
  const question = questions[Math.floor(Math.random() * questions.length)]
  loadQuestionUI(question)
}

function initializeInteractions(questionObj) {
  const options = document.querySelectorAll('.option-btn')
  const submitBtn = document.querySelector('.submit-btn')
  const confidenceButtons = document.querySelectorAll('.confidence-btn')

  function updateSubmitState() {
    submitBtn.disabled = !(selectedAnswers.size > 0 && selectedConfidence)
  }

  options.forEach(btn => {
    btn.addEventListener('click', () => {
      const value = btn.dataset.value

      if (questionObj.multi) {
        if (selectedAnswers.has(value)) {
          selectedAnswers.delete(value)
          btn.classList.remove('selected')
        } else {
          selectedAnswers.add(value)
          btn.classList.add('selected')
        }
      } else {
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

function evaluateAnswer(questionObj) {
  const options = document.querySelectorAll('.option-btn')
  const correctSet = new Set(questionObj.correct)

  const fullyCorrect = selectedAnswers.size === correctSet.size &&
    [...selectedAnswers].every(ans => correctSet.has(ans))

  options.forEach(btn => {
    const value = btn.dataset.value
    if (correctSet.has(value)) btn.classList.add('correct')
    if (selectedAnswers.has(value) && !correctSet.has(value)) btn.classList.add('incorrect')
    btn.disabled = true
  })

  const responseTime = (Date.now() - questionStartTime) / 1000
  const speedWeight = Math.max(0.5, 2 - responseTime / 5)
  const confidenceWeight = typeof selectedConfidence === 'number' ? selectedConfidence : 0.8
  const signalStrength = speedWeight * confidenceWeight

  if (isCustomTest) {
    attemptLog.push({
      question: questionObj.question_text,
      selected: [...selectedAnswers],
      correct: questionObj.correct,
      wasCorrect: fullyCorrect
    })

    setTimeout(() => {
      loadCustomQuestion()
    }, 800)
    return
  }

  updateCognitiveMastery(currentConcept, fullyCorrect, signalStrength)
  conceptStatus[currentConcept] = true

  setTimeout(loadNextConcept, 800)
}

function showResults() {
  const recalculatedRisk = calculateRisk()
  updateStudentState({ risk: recalculatedRisk })

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

    currentUser.completedTests.push(attemptData)

    if (currentUser.activeClass) {
      saveTestAttempt(currentUser.activeClass, currentUser.id, attemptData)
    }

    currentUser.data = getStudentState()
    renderTestBreakdown(activeTestId)

    isCustomTest = false
    attemptLog = []
    activeTestId = null
    return
  }

  currentUser.hasTakenQuiz = true
  currentUser.data = getStudentState()
  renderStudentDashboard(currentUser.data)
}

export async function renderCustomTest(test) {
  isCustomTest = true
  activeTestId = test.id
  attemptLog = []
  customQuestionIndex = 0
  currentConcept = test.topic

  try {
    const allQuestions = await fetchAllQuestions()
    const topicQuestions = allQuestions[test.topic] || []
    
    if (topicQuestions.length === 0) {
      alert(`No questions available for ${test.topic}`)
      return
    }

    customQuestions = []
    for (let i = 0; i < test.numQuestions && i < topicQuestions.length; i++) {
      const randomIndex = Math.floor(Math.random() * topicQuestions.length)
      customQuestions.push(topicQuestions[randomIndex])
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
  } catch (error) {
    console.error("Failed to load custom test:", error)
    alert("Failed to load test. Please try again.")
  }
}

function loadCustomQuestion() {
  if (customQuestionIndex >= customQuestions.length) {
    showResults()
    return
  }

  const question = customQuestions[customQuestionIndex]
  loadQuestionUI(question)
  customQuestionIndex++
}

function loadQuestionUI(question) {
  const quizCard = document.getElementById('quizCard')

  questionStartTime = Date.now()
  selectedAnswers = new Set()
  selectedConfidence = null

  quizCard.innerHTML = `
    <div class="question-text">${question.question_text || question.question}</div>

    ${question.multi ? `<div class="multi-hint">Select all that apply.</div>` : ''}

    <div class="options">
      ${(question.options || []).map(opt => `
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
