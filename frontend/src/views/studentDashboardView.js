import { createMasteryChart, updateMasteryChart } from '../components/charts/masteryChart.js'
import { createRiskRing, updateRiskRing } from '../components/indicators/riskRing.js'
import { renderStudentHome } from './studentHomeView.js'

export function renderStudentDashboard(data) {
  const app = document.getElementById('app')

  const weakestConcept =
    Object.entries(data.mastery)
      .sort((a, b) => a[1].value - b[1].value)[0][0]

  app.innerHTML = `
    <div class="background-glow"></div>

    <div class="dashboard-container">

      <div class="glass-panel dashboard-header">
        <h1 class="dashboard-title">Student Cognitive Dashboard</h1>
        <button id="backBtn" class="glass-btn">Back to Home</button>
      </div>

      <div class="dashboard-grid">

        <div class="glass-panel">
          <h2>Concept Mastery</h2>
          <canvas id="masteryChart"></canvas>
        </div>

        <div class="glass-panel risk-panel">
          <h2>Risk Prediction</h2>

          <div id="riskContainer" class="risk-ring-wrapper"></div>

          <div class="weakest-indicator">
            Weakest Concept:
            <span class="weak-highlight">${weakestConcept}</span>
          </div>
        </div>

      </div>

    </div>
  `

  /* ============================= */
  /* MASTERy CHART */
  /* ============================= */

  createMasteryChart('masteryChart')

  updateMasteryChart([
    data.mastery.Binomial.value,
    data.mastery.Poisson.value,
    data.mastery.Normal.value,
    data.mastery.Bayes.value,
    data.mastery.Conditional.value
  ])

  /* ============================= */
  /* RISK RING (Animated) */
  /* ============================= */

  createRiskRing('riskContainer', 0)

  // small delay so animation feels smooth
  setTimeout(() => {
    updateRiskRing(Math.round(data.risk))
  }, 200)

  /* ============================= */
  /* NAVIGATION */
  /* ============================= */

  document
    .getElementById('backBtn')
    .addEventListener('click', renderStudentHome)
}