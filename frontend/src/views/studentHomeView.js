import { renderStudentDashboard } from './studentDashboardView.js'
import { renderQuiz } from '../student/quiz.js'
import { currentUser } from '../testApp.js'

export function renderStudentHome() {
  const app = document.getElementById('app')

  app.innerHTML = `
    <div class="dashboard-container">
      <h1>Student Portal</h1>

      <button id="viewDashboard">View Dashboard</button>
      <button id="takeQuiz">Take Diagnostic Quiz</button>
    </div>
  `

  document.getElementById('viewDashboard').onclick = () => {
    if (!currentUser.hasTakenQuiz) {
      app.innerHTML = `
        <div class="dashboard-container">
          <h1>No Assessment Data Yet</h1>
          <p>You haven't taken a diagnostic yet.</p>
          <button id="backBtn">Back</button>
        </div>
      `
      document.getElementById('backBtn')
        .onclick = renderStudentHome
    } else {
      renderStudentDashboard(currentUser.data)
    }
  }

  document.getElementById('takeQuiz').onclick = renderQuiz
}