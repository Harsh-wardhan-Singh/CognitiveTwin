import { createMasteryChart, updateMasteryChart } from '../components/charts/masteryChart.js'
import { createRiskRing, updateRiskRing } from '../components/indicators/riskRing.js'
import { getStudentState } from '../services/state.js'
import { renderTeacherDashboard } from '../teacher/teacherDashboard.js'

export function renderDashboard() {
  const app = document.getElementById('app')
  const data = getStudentState()

  // Fix weakest concept logic
  const weakestConcept =
    Object.entries(data.mastery)
      .sort((a, b) => a[1].value - b[1].value)[0][0]

  app.innerHTML = `
    <div class="background-glow"></div>

    <div class="dashboard-container">
      <h1 class="dashboard-title">Student Cognitive Dashboard</h1>

      <button id="teacherBtn" class="submit-btn" style="margin-bottom:20px;">
        Switch to Teacher View
      </button>

      <div class="dashboard-grid">
        <div class="card">
          <h2>Concept Mastery</h2>
          <canvas id="masteryChart"></canvas>
        </div>

        <div class="card">
          <h2>Risk Prediction</h2>
          <div id="riskContainer"></div>

          <div class="weakest-indicator">
            Weakest Concept: 
            <span id="weakestConcept">${weakestConcept}</span>
          </div>
        </div>

        <div class="card full-width">
          <h2>Recent Attempts</h2>
          <div class="attempts-placeholder">
            Performance data will appear here.
          </div>
        </div>
      </div>
    </div>
  `

  initializeDashboard(data)

  document
    .getElementById('teacherBtn')
    .addEventListener('click', renderTeacherDashboard)
}

function initializeDashboard(data) {
  createMasteryChart('masteryChart')
  createRiskRing('riskContainer', 0)

  // Extract numeric mastery values correctly
  updateMasteryChart([
    data.mastery.Binomial.value,
    data.mastery.Poisson.value,
    data.mastery.Normal.value,
    data.mastery.Bayes.value,
    data.mastery.Conditional.value
  ])

  updateRiskRing(Math.round(data.risk))
}