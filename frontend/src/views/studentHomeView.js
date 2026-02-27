import { getTestsForClassroom } from '../services/testStore.js'
import { currentUser, mountView } from '../testApp.js'
import { renderStudentDashboard } from './studentDashboardView.js'
import { renderQuiz, renderCustomTest } from '../student/quiz.js'
import { fetchStudentClassrooms, joinClassroom as joinClassroomAPI } from '../services/api.js'

/* ============================= */
/* MAIN STUDENT HOME */
/* ============================= */

export async function renderStudentHome(forceClassCode = null) {

  if (forceClassCode) {
    currentUser.activeClass = forceClassCode
  }

  if (currentUser.activeClass) {
    renderStudentClassroomView()
    return
  }

  mountView((container) => {

    container.innerHTML = `
      <div class="dashboard-container">
        <h1>Your Classrooms</h1>

        <div class="glass-panel" style="margin-bottom:20px;">
          <input
            id="joinCode"
            placeholder="Enter Classroom ID or Code"
            style="padding:8px;"
          />

          <button id="joinBtn" class="glass-btn" style="margin-left:10px;">
            Join Classroom
          </button>
        </div>

        <div id="classList"></div>
      </div>
    `

    const classList =
      document.getElementById('classList')

    // Fetch classrooms from backend
    fetchStudentClassrooms().then(classrooms => {
      if (classrooms.length === 0) {
        classList.innerHTML =
          "<p>No classrooms joined yet.</p>"
      } else {
        classList.innerHTML =
          classrooms.map(c => `
            <div class="glass-panel clickable"
                 data-id="${c.id}">
              ${c.name || 'Classroom'}<br/>
              <small>${c.subject || 'N/A'}</small>
            </div>
          `).join('')
        
        document
          .querySelectorAll('[data-id]')
          .forEach(panel => {
            panel.addEventListener('click', () => {
              currentUser.activeClass =
                panel.dataset.id
              renderStudentClassroomView()
            })
          })
      }
    }).catch(err => {
      console.error("Failed to load classrooms:", err)
      classList.innerHTML = "<p>Error loading classrooms</p>"
    })

    document
      .getElementById('joinBtn')
      .addEventListener('click', async () => {

        const code =
          document.getElementById('joinCode')
            .value.trim()

        if (!code) {
          alert("Please enter a classroom ID")
          return
        }

        try {
          // Try to join using the code as classroom ID
          await joinClassroomAPI(parseInt(code) || code)
          currentUser.activeClass = code
          renderStudentHome()
        } catch (err) {
          alert("Failed to join classroom: " + err.message)
        }
      })
  })
}

/* ============================= */
/* CLASSROOM VIEW */
/* ============================= */

function renderStudentClassroomView() {

  mountView((container) => {

    const tests =
      getTestsForClassroom(currentUser.activeClass)

    container.innerHTML = `
      <div class="dashboard-container">

        <button id="backBtn" class="glass-btn" style="margin-bottom:20px;">
          Back to Classrooms
        </button>

        <h1>Classroom ${currentUser.activeClass}</h1>

        <div class="glass-panel" style="margin-bottom:20px;">
          <button id="takeDiagnostic" class="glass-btn">
            Take Diagnostic
          </button>

          <button id="viewDashboard"
                  class="glass-btn"
                  style="margin-left:10px;">
            View Dashboard
          </button>
        </div>

        <div id="availableTests"></div>
      </div>
    `

    document
      .getElementById('backBtn')
      .addEventListener('click', () => {
        currentUser.activeClass = null
        renderStudentHome()
      })

    document
      .getElementById('takeDiagnostic')
      .addEventListener('click', renderQuiz)

    document
      .getElementById('viewDashboard')
      .addEventListener('click', () => {

        if (!currentUser.hasTakenQuiz) {
          alert("Take a diagnostic first.")
          return
        }

        renderStudentDashboard(currentUser.data)
      })

    /* ============================= */
    /* AVAILABLE TESTS */
    /* ============================= */

    const testContainer =
      document.getElementById('availableTests')

    if (tests.length === 0) {
      testContainer.innerHTML =
        "<p>No tests available.</p>"
      return
    }

    testContainer.innerHTML = `
      <h3>Available Tests</h3>
      ${tests.map(test => {

        const alreadyTaken =
          currentUser.completedTests?.some(
            t => t.testId === test.id
          )

        return `
          <div class="glass-panel clickable
                      ${alreadyTaken ? 'disabled-test' : ''}"
               data-id="${test.id}"
               data-taken="${alreadyTaken}">
            Topic: ${test.topic}<br/>
            Difficulty: ${test.difficulty}<br/>
            Questions: ${test.numQuestions}
            ${alreadyTaken ? '<br/><strong>Completed</strong>' : ''}
          </div>
        `
      }).join('')}
    `

    document
      .querySelectorAll('[data-id]')
      .forEach(panel => {

        panel.addEventListener('click', () => {

          const testId = panel.dataset.id
          const alreadyTaken =
            panel.dataset.taken === 'true'

          if (alreadyTaken) {
            renderTestBreakdown(testId)
            return
          }

          if (!currentUser.hasTakenQuiz) {
            alert("You must complete the diagnostic first.")
            return
          }

          const test =
            tests.find(t => t.id === testId)

          renderCustomTest(test)
        })
      })
  })
}

/* ============================= */
/* TEST BREAKDOWN VIEW */
/* ============================= */

export function renderTestBreakdown(testId) {

  const attempt =
    currentUser.completedTests
      .find(t => t.testId === testId)

  mountView((container) => {

    container.innerHTML = `
  <div class="dashboard-container">

    <div style="margin-bottom:20px;">
      <button id="backBtn" class="glass-btn">
        Back to Classroom
      </button>

      <button id="dashboardBtn"
              class="glass-btn"
              style="margin-left:10px;">
        View Dashboard
      </button>
    </div>

    <h1>${attempt.topic} Test Breakdown</h1>

    <h3>
      Score: ${attempt.score}/${attempt.total}
    </h3>

    <div id="breakdownList"></div>
  </div>
`

    const breakdown =
      document.getElementById('breakdownList')

    breakdown.innerHTML =
      attempt.questions.map((q, index) => `
        <div class="glass-panel"
             style="margin-bottom:15px;">
          <strong>Question ${index + 1}</strong>
          <p>${q.question}</p>

          <p><strong>Your Answer:</strong>
             ${q.selected.join(', ')}</p>

          <p><strong>Correct Answer:</strong>
             ${q.correct.join(', ')}</p>

          <p>
            <strong>
              ${q.wasCorrect ? 'Correct' : 'Incorrect'}
            </strong>
          </p>

          <p><em>${q.explanation}</em></p>
        </div>
      `).join('')

    document
      .getElementById('backBtn')
      .addEventListener('click', () => {
        renderStudentClassroomView()
      })

      document
  .getElementById('dashboardBtn')
  .addEventListener('click', () => {
    renderStudentDashboard(currentUser.data)
  })
  })
}