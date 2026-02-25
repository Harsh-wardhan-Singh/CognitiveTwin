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
      <div id="heatmap" class="heatmap"></div>
    </div>
  `

  renderHeatmap(classData)
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