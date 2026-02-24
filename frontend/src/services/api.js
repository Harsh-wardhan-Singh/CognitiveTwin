/* =====================================================
   API SERVICE LAYER
   ===================================================== */

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

/**
 * Simulated fetch for dashboard data
 * Later this becomes real fetch()
 */
export async function fetchStudentDashboard() {
  // Simulate network delay
  await delay(800)

  return {
    mastery: [82, 72, 78, 65, 80],
    risk: 26,
    attempts: [
      { topic: "Binomial", score: 85 },
      { topic: "Poisson", score: 70 }
    ]
  }
}

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms))
}