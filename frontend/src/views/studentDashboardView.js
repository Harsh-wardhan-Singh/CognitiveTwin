import { createMasteryChart, updateMasteryChart } from '../components/charts/masteryChart.js'
import { createRiskRing, updateRiskRing } from '../components/indicators/riskRing.js'
import { renderStudentHome } from './studentHomeView.js'
import { mountView, currentUser } from '../testApp.js'
import { fetchStudentDashboard } from '../services/api.js'

export async function renderStudentDashboard(data) {
  
  // If data is not provided or empty, fetch from backend
  if (!data || !data.mastery || Object.keys(data.mastery).length === 0) {
    try {
      const backendData = await fetchStudentDashboard()
      if (backendData) {
        data = {
          mastery: backendData.mastery || {},
          risk: backendData.risk_score || 0
        }
        currentUser.data = data
      }
    } catch (error) {
      console.error("Failed to fetch dashboard data:", error)
      // Use default empty state if fetch fails
      data = {
        mastery: {
          Binomial: { value: 50 },
          Poisson: { value: 50 },
          Normal: { value: 50 },
          Bayes: { value: 50 },
          Conditional: { value: 50 }
        },
        risk: 0
      }
    }
  }

  mountView((container) => {

    const weakestConcept =
      Object.entries(data.mastery)
        .sort((a, b) => a[1].value - b[1].value)[0][0]

    container.innerHTML = `
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
    /* MASTERY CHART */
    /* ============================= */

    createMasteryChart('masteryChart')

    updateMasteryChart([
      data.mastery.Binomial?.value || 50,
      data.mastery.Poisson?.value || 50,
      data.mastery.Normal?.value || 50,
      data.mastery.Bayes?.value || 50,
      data.mastery.Conditional?.value || 50
    ])

    /* ============================= */
    /* RISK RING */
    /* ============================= */

    createRiskRing('riskContainer', 0)

    setTimeout(() => {
      updateRiskRing(Math.round(data.risk))
    }, 200)

    /* ============================= */
    /* NAVIGATION */
    /* ============================= */

    document
      .getElementById('backBtn')
      .addEventListener('click', () => {
        // If student is inside a classroom,
        // go back to that classroom instead of selection screen
        renderStudentHome(currentUser.activeClass)
      })

  })
}