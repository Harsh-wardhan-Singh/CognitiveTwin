import { getStudentState } from '../services/state.js'
import { generateClassData } from './analytics.js'
import './teacher.css'

export function renderTeacherDashboard() {
  const container = document.getElementById('teacherContent')

  const baseMastery = getStudentState().mastery
  const classData = generateClassData(baseMastery, 20)

  container.innerHTML = `
  <div class="teacher-container">
    <h1 class="teacher-title">Class Cognitive Overview</h1>

    <div class="class-summary" id="classSummary"></div>

    <div class="teacher-insights" id="teacherInsights"></div>

    <div id="heatmap" class="heatmap"></div>
  </div>
`

  renderHeatmap(classData)
  renderInsights(classData)
  renderClassSummary(classData)
}

/* ============================= */
/* HEATMAP */
/* ============================= */

function renderHeatmap(classData) {
  const heatmap = document.getElementById('heatmap')
  const concepts = Object.keys(classData[0].mastery)

  let html = `
    <div class="heatmap-row header">
      <div class="heatmap-cell">Student</div>
      ${concepts.map(c => `<div class="heatmap-cell">${c}</div>`).join('')}
      <div class="heatmap-cell">Risk</div>
    </div>
  `

  classData.forEach(student => {
    const values = Object.values(student.mastery).map(m => m.value)
    const max = Math.max(...values)
    const min = Math.min(...values)
    const isUnstable = (max - min) > 25

    html += `
      <div class="heatmap-row ${isUnstable ? 'unstable-row' : ''}">
        <div class="heatmap-cell student-id clickable"
             data-student="${student.id}">
          ${student.id}
        </div>

        ${concepts.map(c => `
          <div class="heatmap-cell mastery"
            style="background-color: ${getColor(student.mastery[c].value)}">
            ${Math.round(student.mastery[c].value)}
          </div>
        `).join('')}

        <div class="heatmap-cell risk"
          style="background-color: ${getRiskColor(student.risk)}">
          ${Math.round(student.risk)}
        </div>
      </div>
    `
  })

  heatmap.innerHTML = html

  // Attach click listeners AFTER DOM is created
  document.querySelectorAll('.student-id.clickable')
    .forEach(cell => {
      cell.addEventListener('click', () => {
        const studentId = cell.dataset.student
        openStudentDetail(studentId, classData)
      })
    })
}

/* ============================= */
/* INSIGHTS */
/* ============================= */

function renderInsights(classData) {
  const container = document.getElementById('teacherInsights')

  const risks = classData.map(s => s.risk)

  const highRisk = risks.filter(r => r > 70).length
  const moderateRisk = risks.filter(r => r > 40 && r <= 70).length
  const lowRisk = risks.filter(r => r <= 40).length

  const conceptCounts = {}

  classData.forEach(student => {
    const weakest =
      Object.entries(student.mastery)
        .sort((a, b) => a[1].value - b[1].value)[0][0]

    conceptCounts[weakest] =
      (conceptCounts[weakest] || 0) + 1
  })

  const mostProblematicConcept =
    Object.entries(conceptCounts)
      .sort((a, b) => b[1] - a[1])[0][0]

  const unstableStudents = classData.filter(student => {
    const values =
      Object.values(student.mastery).map(m => m.value)

    const max = Math.max(...values)
    const min = Math.min(...values)

    return (max - min) > 25
  }).length

  container.innerHTML = `
    <div class="insight-card">
      <h3>Risk Distribution</h3>
      <p>High: ${highRisk}</p>
      <p>Moderate: ${moderateRisk}</p>
      <p>Low: ${lowRisk}</p>
    </div>

    <div class="insight-card">
      <h3>Most Problematic Concept</h3>
      <p>${mostProblematicConcept}</p>
    </div>

    <div class="insight-card">
      <h3>High Risk Students</h3>
      <p>${highRisk} students above 70%</p>
    </div>

    <div class="insight-card">
      <h3>Instability Alerts</h3>
      <p>${unstableStudents} students highly unstable</p>
    </div>
  `
}

function renderClassSummary(classData) {
  const summary = document.getElementById('classSummary')

  const conceptAverages = {}

  Object.keys(classData[0].mastery).forEach(concept => {
    const avg =
      classData
        .map(s => s.mastery[concept].value)
        .reduce((a, b) => a + b, 0) / classData.length

    conceptAverages[concept] = avg
  })

  const weakestConcept =
    Object.entries(conceptAverages)
      .sort((a, b) => a[1] - b[1])[0][0]

  const avgRisk =
    classData
      .map(s => s.risk)
      .reduce((a, b) => a + b, 0) / classData.length

  summary.innerHTML = `
    <div class="insight-card">
      <h3>Class Average Risk</h3>
      <p>${Math.round(avgRisk)}%</p>
    </div>

    <div class="insight-card">
      <h3>Most Struggled Concept</h3>
      <p>${weakestConcept}</p>
    </div>

    <div class="insight-card">
      <h3>Concept Averages</h3>
      ${Object.entries(conceptAverages).map(
        ([concept, value]) =>
          `<div>${concept}: ${Math.round(value)}%</div>`
      ).join('')}
    </div>
  `
}

/* ============================= */
/* COLOR HELPERS */
/* ============================= */

function getColor(value) {
  const red = Math.round(255 - (value * 2.5))
  const green = Math.round(value * 2.5)
  return `rgb(${red}, ${green}, 80)`
}

function getRiskColor(value) {
  const red = Math.round(value * 2.5)
  const green = Math.round(255 - value * 2.5)
  return `rgb(${red}, ${green}, 80)`
}
import { createMasteryChart, updateMasteryChart } from '../components/charts/masteryChart.js'
import { createRiskRing, updateRiskRing } from '../components/indicators/riskRing.js'

function openStudentDetail(studentId, classData) {
  const student = classData.find(s => s.id === studentId)
  const container = document.getElementById('teacherContent')

  const masteryEntries = Object.entries(student.mastery)

  const weakestEntry =
    masteryEntries.sort((a, b) => a[1].value - b[1].value)[0]

  const weakestConcept = weakestEntry[0]
  const weakestScore = weakestEntry[1].value

  const explanation =
    generateExplanation(weakestConcept, weakestScore, student.risk)

  container.innerHTML = `
    <div class="glass-panel detail-header">
      <h2>Student ${student.id}</h2>
      <button id="backToClass" class="glass-btn">
        Back to Class Overview
      </button>
    </div>

    <div class="dashboard-grid detail-grid">

      <div class="glass-panel">
        <h3>Concept Mastery</h3>
        <canvas id="teacherMasteryChart"></canvas>
      </div>

      <div class="glass-panel">
        <h3>Risk Prediction</h3>
        <div id="teacherRiskRing"></div>
      </div>

    </div>

    <div class="glass-panel explanation-panel">
      <h3>Cognitive Insight</h3>
      <p><strong>Primary Weakness:</strong> ${weakestConcept}</p>
      <p>${explanation}</p>
    </div>
  `

  /* Render Chart */
  createMasteryChart('teacherMasteryChart')

  updateMasteryChart([
    student.mastery.Binomial.value,
    student.mastery.Poisson.value,
    student.mastery.Normal.value,
    student.mastery.Bayes.value,
    student.mastery.Conditional.value
  ])

  /* Render Risk */
  createRiskRing('teacherRiskRing', 0)

  setTimeout(() => {
    updateRiskRing(Math.round(student.risk))
  }, 200)

  document
    .getElementById('backToClass')
    .addEventListener('click', renderTeacherDashboard)
}

function generateExplanation(concept, score, risk) {
  if (risk > 70) {
    return `High cognitive risk detected. ${concept} mastery is significantly low (${Math.round(score)}%). Immediate intervention recommended.`
  }

  if (score < 50) {
    return `Student shows conceptual gaps in ${concept}. Likely misunderstanding foundational reasoning patterns.`
  }

  if (score < 70) {
    return `Moderate instability in ${concept}. Performance inconsistent — may benefit from targeted reinforcement.`
  }

  return `No critical conceptual risk detected in ${concept}, but monitoring recommended.`
}