import { getStudentState } from '../services/state.js'
import { generateClassData } from './analytics.js'
import './teacher.css'

export function renderTeacherDashboard() {
  const app = document.getElementById('app')

  const baseMastery = getStudentState().mastery
  const classData = generateClassData(baseMastery, 20)

  app.innerHTML = `
  <div class="teacher-container">
    <h1 class="teacher-title">Class Cognitive Overview</h1>

    <div class="teacher-insights" id="teacherInsights"></div>

    <div id="heatmap" class="heatmap"></div>
  </div>
`

  renderHeatmap(classData)
  renderInsights(classData)
}

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
    html += `
      <div class="heatmap-row">
        <div class="heatmap-cell student-id">${student.id}</div>
        ${concepts.map(c => `
          <div class="heatmap-cell mastery"
            style="background-color: ${getColor(student.mastery[c])}">
            ${Math.round(student.mastery[c])}
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
}

function renderInsights(classData) {
  const container = document.getElementById('teacherInsights')

  const risks = classData.map(s => s.risk)

  const highRisk = risks.filter(r => r > 70).length
  const moderateRisk = risks.filter(r => r > 40 && r <= 70).length
  const lowRisk = risks.filter(r => r <= 40).length

  const conceptCounts = {}

  classData.forEach(student => {
    const weakest = Object.entries(student.mastery)
      .sort((a, b) => a[1] - b[1])[0][0]

    conceptCounts[weakest] = (conceptCounts[weakest] || 0) + 1
  })

  const mostProblematicConcept =
    Object.entries(conceptCounts)
      .sort((a, b) => b[1] - a[1])[0][0]

  // ✅ DECLARE BEFORE USE
  const unstableStudents = classData.filter(student => {
    const values = Object.values(student.mastery)
    const max = Math.max(...values)
    const min = Math.min(...values)
    return (max - min) > 40
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