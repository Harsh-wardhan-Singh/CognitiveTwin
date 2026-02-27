import { renderTeacherDashboard } from '../teacher/teacherDashboard.js'
import { renderTeacherClassSelect } from './teacherClassSelectView.js'
import { createTest, getTestsForClassroom } from '../services/testStore.js'
import { getClassroomById } from '../services/classroomStore.js'
import { currentUser } from '../testApp.js'

export function renderTeacherClassView() {

  const app = document.getElementById('appContent')

  app.innerHTML = `
    <div class="teacher-container">

      <button id="backToClasses" class="glass-btn" style="margin-bottom:20px;">
        Back to Classrooms
      </button>

      <div class="glass-panel" style="margin-bottom:20px;">
        <h2>Create Test</h2>

        <button id="createTestBtn" class="glass-btn">
          New Test
        </button>

        <div id="testCreator" style="margin-top:15px; display:none;">
          
          <select id="testTopic">
            <option value="Binomial">Binomial</option>
            <option value="Poisson">Poisson</option>
            <option value="Normal">Normal</option>
            <option value="Bayes">Bayes</option>
            <option value="Conditional">Conditional</option>
          </select>

          <select id="testDifficulty" style="margin-left:10px;">
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>

          <input 
            id="numQuestions"
            type="number"
            min="1"
            max="10"
            value="3"
            style="width:80px; margin-left:10px;"
          />

          <button id="submitTest" class="glass-btn" style="margin-left:10px;">
            Create
          </button>
        </div>
      </div>

      <div id="teacherContent"></div>

    </div>
  `

  /* ============================= */
  /* INITIAL DASHBOARD + TEST LIST */
  /* ============================= */

  renderTeacherDashboard()
  renderTeacherTestList(currentUser.activeClass)

  /* ============================= */
  /* NAVIGATION */
  /* ============================= */

  document
    .getElementById('backToClasses')
    .addEventListener('click', renderTeacherClassSelect)

  document
    .getElementById('createTestBtn')
    .addEventListener('click', () => {
      document.getElementById('testCreator').style.display = 'block'
    })

  /* ============================= */
  /* CREATE TEST */
  /* ============================= */

  document
    .getElementById('submitTest')
    .addEventListener('click', () => {

      const topic = document.getElementById('testTopic').value
      const difficulty = document.getElementById('testDifficulty').value
      const numQuestions = parseInt(
        document.getElementById('numQuestions').value
      )

      createTest({
        classroomId: currentUser.activeClass,
        topic,
        difficulty,
        numQuestions
      })

      alert("Test created successfully.")

      document.getElementById('testCreator').style.display = 'none'

      // 🔥 Refresh test list
      document.getElementById('teacherContent').innerHTML = ""
      renderTeacherTestList(currentUser.activeClass)
    })
}


/* ============================= */
/* TEST LIST */
/* ============================= */

function renderTeacherTestList(classCode) {

  const tests = getTestsForClassroom(classCode)

  const container = document.getElementById('teacherContent')

  container.innerHTML += `
    <h2 style="margin-top:30px;">Created Tests</h2>
    <div id="teacherTestList"></div>
  `

  const list = document.getElementById('teacherTestList')

  if (tests.length === 0) {
    list.innerHTML = "<p>No tests created.</p>"
    return
  }

  list.innerHTML = tests.map(test => `
    <div class="glass-panel clickable"
         data-id="${test.id}">
      ${test.topic} (${test.difficulty})
    </div>
  `).join('')

  document
  .querySelectorAll('#teacherTestList [data-id]')
  .forEach(panel => {
    panel.addEventListener('click', () => {
      renderTeacherTestPerformance(
        classCode,
        panel.dataset.id
      )
    })
  })
}


/* ============================= */
/* TEST PERFORMANCE */
/* ============================= */

function renderTeacherTestPerformance(classCode, testId) {

  const classroom = getClassroomById(classCode)

  //  Safety checks
  if (!classroom) {
    console.error("Classroom not found:", classCode)
    return
  }

  if (!classroom.testAttempts) {
    classroom.testAttempts = []
  }

  const attempts =
    classroom.testAttempts.filter(
      a => a.testId === testId
    )

  const container =
    document.getElementById('teacherContent')

  container.innerHTML = `
    <button id="backBtn" class="glass-btn"
            style="margin-bottom:20px;">
      Back
    </button>

    <h2>Test Performance</h2>

    <div id="studentResults"></div>
  `

  const results =
    document.getElementById('studentResults')

  if (attempts.length === 0) {

    results.innerHTML =
      "<p>No students have taken this test.</p>"

  } else {

    results.innerHTML =
      attempts.map(a => `
        <div class="glass-panel clickable"
             data-student="${a.studentId}">
          Student: ${a.studentId}
          <br/>
          Score: ${a.score}/${a.total}
        </div>
      `).join('')
  }

  // Attach student click handlers safely
  document
    .querySelectorAll('#studentResults [data-student]')
    .forEach(panel => {
      panel.addEventListener('click', () => {

        const selectedAttempt =
          attempts.find(
            a => a.studentId === panel.dataset.student
          )

        if (!selectedAttempt) return

        renderTeacherStudentBreakdown(selectedAttempt)
      })
    })

  document
    .getElementById('backBtn')
    .addEventListener('click', () => {
      renderTeacherClassView()
    })
}


/* ============================= */
/* STUDENT BREAKDOWN */
/* ============================= */

function renderTeacherStudentBreakdown(attempt) {

  const container =
    document.getElementById('teacherContent')

  container.innerHTML = `
    <button id="backBtn" class="glass-btn"
            style="margin-bottom:20px;">
      Back
    </button>

    <h2>Student ${attempt.studentId}</h2>

    <h3>Score: ${attempt.score}/${attempt.total}</h3>

    <div id="breakdown"></div>
  `

  const breakdown =
    document.getElementById('breakdown')

  breakdown.innerHTML =
    attempt.questions.map((q, index) => `
      <div class="glass-panel"
           style="margin-bottom:15px;">
        <strong>Question ${index + 1}</strong>
        <p>${q.question}</p>
        <p>Selected: ${q.selected.join(', ')}</p>
        <p>Correct: ${q.correct.join(', ')}</p>
        <p>${q.wasCorrect ? 'Correct' : 'Incorrect'}</p>
      </div>
    `).join('')

  document.getElementById('backBtn')
    .addEventListener('click', () => {
      renderTeacherClassView()
    })
}