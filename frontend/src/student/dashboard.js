import { createMasteryChart, updateMasteryChart } from '../components/charts/masteryChart.js'
import { createRiskRing, updateRiskRing } from '../components/indicators/riskRing.js'
import { getStudentState } from '../services/state.js'

export function renderDashboard() {
  const app = document.getElementById('app')

  app.innerHTML = `
    <div class="background-glow"></div>

    <div class="dashboard-container">
      <h1 class="dashboard-title">Student Cognitive Dashboard</h1>

      <div class="dashboard-grid">
        <div class="card">
          <h2>Concept Mastery</h2>
          <canvas id="masteryChart"></canvas>
        </div>

        <div class="card">
          <h2>Risk Prediction</h2>
          <div id="riskContainer"></div>
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

  initializeDashboard()
}

function initializeDashboard() {
  const data = getStudentState()

  // SAFETY CHECKS
  const chartCanvas = document.getElementById('masteryChart')
  const riskContainer = document.getElementById('riskContainer')

  if (!chartCanvas || !riskContainer) {
    console.error("Dashboard elements not found.")
    return
  }

  createMasteryChart('masteryChart')
  createRiskRing('riskContainer', 0)

  updateMasteryChart(data.mastery)
  updateRiskRing(Math.round(data.risk))
}