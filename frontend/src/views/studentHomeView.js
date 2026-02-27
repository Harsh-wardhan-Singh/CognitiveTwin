import { joinClassroom, getStudentClassrooms } from '../services/classroomStore.js'
import { currentUser } from '../testApp.js'
import { renderStudentDashboard } from './studentDashboardView.js'
import { renderQuiz } from '../student/quiz.js'
import { mountView } from '../testApp.js'

export function renderStudentHome() {

  mountView((container) => {

    const classrooms = getStudentClassrooms(currentUser.id)

    container.innerHTML = `
      <div class="dashboard-container">
        <h1>Select Classroom</h1>

        <div id="classList"></div>

        <hr style="margin:30px 0;" />

        <input
          id="joinCode"
          placeholder="Enter Classroom Code"
          style="padding:8px; margin-bottom:10px;"
        />

        <button id="joinBtn" class="glass-btn">
          Join Classroom
        </button>
      </div>
    `

    const classList = container.querySelector('#classList')

    if (classrooms.length === 0) {
      classList.innerHTML = `<p>You have not joined any classrooms yet.</p>`
    } else {
      classList.innerHTML = classrooms.map(c => `
        <div class="glass-panel clickable"
             data-code="${c.id}">
          Classroom Code: ${c.id}
        </div>
      `).join('')
    }

    /* ============================= */
    /* JOIN CLASSROOM */
    /* ============================= */

    container.querySelector('#joinBtn')
      .addEventListener('click', () => {
        const code = container.querySelector('#joinCode').value.trim()

        const classroom = joinClassroom(code, currentUser.id)

        if (!classroom) {
          alert("Invalid classroom code.")
          return
        }

        alert("Joined classroom successfully!")
        renderStudentHome()
      })

    /* ============================= */
    /* SELECT CLASSROOM */
    /* ============================= */

    container.querySelectorAll('.clickable')
      .forEach(panel => {
        panel.addEventListener('click', () => {
          currentUser.activeClass = panel.dataset.code
          renderStudentPortal()
        })
      })

  })
}

/* ============================= */
/* STUDENT PORTAL AFTER SELECT */
/* ============================= */

export function renderStudentPortal() {

  mountView((container) => {

    container.innerHTML = `
      <div class="dashboard-container">
        <h1>Classroom: ${currentUser.activeClass}</h1>

        <button id="dashboardBtn" class="glass-btn">
          View Dashboard
        </button>

        <button id="quizBtn" class="glass-btn" style="margin-left:10px;">
          Take Diagnostic
        </button>

        <br/><br/>

        <button id="backBtn" class="glass-btn">
          Back to Class Selection
        </button>
      </div>
    `

    container.querySelector('#dashboardBtn')
      .addEventListener('click', () => {
        if (!currentUser.hasTakenQuiz) {
          alert("Take a diagnostic first.")
          return
        }

        renderStudentDashboard(currentUser.data)
      })

    container.querySelector('#quizBtn')
      .addEventListener('click', renderQuiz)

    container.querySelector('#backBtn')
      .addEventListener('click', renderStudentHome)

  })
}