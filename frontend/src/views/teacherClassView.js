import { renderTeacherDashboard } from '../teacher/teacherDashboard.js'
import { renderTeacherClassSelect } from './teacherClassSelectView.js'
import { createTest, getTestsForClassroom } from '../services/testStore.js'
import { currentUser, mountView } from '../testApp.js'
import { fetchClassroomStudents, API_BASE_URL } from '../services/api.js'

export async function renderTeacherClassView() {

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

      <div id="dashboardContent"></div>
      <div id="testsContent"></div>
      <div id="studentsContent"></div>

    </div>
  `

  /* ============================= */
  /* INITIAL DASHBOARD + TEST LIST + STUDENTS */
  /* ============================= */

  renderTeacherDashboard(currentUser.activeClass)
  renderTeacherTestList(currentUser.activeClass)
  renderEnrolledStudents(currentUser.activeClass)

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
      document.getElementById('testsContent').innerHTML = ""
      renderTeacherTestList(currentUser.activeClass)
    })
}


/* ============================= */
/* TEST LIST */
/* ============================= */

function renderTeacherTestList(classCode) {

  const tests = getTestsForClassroom(classCode)

  const container = document.getElementById('testsContent')

  container.innerHTML = `
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


/* ============================= */
/* ENROLLED STUDENTS */
/* ============================= */

let cachedStudents = []  // Cache to track student risk updates

async function renderEnrolledStudents(classroomId) {
  try {
    const students = await fetchClassroomStudents(classroomId)
    cachedStudents = students  // Store for later updates
    
    const enrolledDiv = document.getElementById('studentsContent')
    if (!enrolledDiv) return
    
    let studentsHTML = `
      <h2 style="margin-top:30px;">Enrolled Students (${students.length})</h2>
      <div id="studentsList"></div>
    `
    
    enrolledDiv.innerHTML = studentsHTML
    
    const studentsList = document.getElementById('studentsList')
    
    if (students.length === 0) {
      studentsList.innerHTML = '<p>No students enrolled yet.</p>'
      return
    }
    
    studentsList.innerHTML = students.map(student => `
      <div class="glass-panel clickable" data-student-id="${student.id}" style="margin-bottom:10px; cursor: pointer;">
        <strong>${student.email}</strong><br/>
        <small>Risk: <span style="color: ${student.risk > 0.6 ? 'red' : student.risk > 0.3 ? 'orange' : 'green'}">
          ${student.risk_level.toUpperCase()} (<span class="risk-value">${(student.risk * 100).toFixed(1)}</span>%)
        </span></small>
      </div>
    `).join('')
    
    // Add click handlers
    attachStudentClickHandlers(classroomId)
  } catch (err) {
    console.error("Failed to load students:", err)
    const enrolledDiv = document.getElementById('studentsContent')
    if (enrolledDiv) {
      enrolledDiv.innerHTML = `<p style="color: red;">Failed to load students: ${err.message}</p>`
    }
  }
}

function attachStudentClickHandlers(classroomId) {
  document.querySelectorAll('#studentsList [data-student-id]').forEach(panel => {
    panel.addEventListener('click', async () => {
      const studentId = panel.dataset.studentId
      try {
        const response = await fetch(`${API_BASE_URL}/teacher/student/${studentId}/dashboard`, {
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include'
        })
        const dashboardData = await response.json()
        
        // Update cached student data with fresh risk
        const studentIndex = cachedStudents.findIndex(s => s.id == studentId)
        if (studentIndex >= 0 && dashboardData.risk_score !== undefined) {
          cachedStudents[studentIndex].risk = dashboardData.risk_score
          cachedStudents[studentIndex].risk_level = dashboardData.risk_score > 0.6 ? 'high' : dashboardData.risk_score > 0.3 ? 'medium' : 'low'
        }
        
        renderStudentDashboardView(dashboardData, studentId, classroomId)
      } catch (err) {
        console.error("Failed to load student dashboard:", err)
        alert("Failed to load student dashboard: " + err.message)
      }
    })
  })
}


/* ============================= */
/* STUDENT DASHBOARD VIEW */
/* ============================= */

function renderStudentDashboardView(data, studentId, classroomId) {
  const container = document.getElementById('dashboardContent')
  const testsContainer = document.getElementById('testsContent')
  const studentsContainer = document.getElementById('studentsContent')
  
  // Hide other sections
  testsContainer.style.display = 'none'
  studentsContainer.style.display = 'none'
  
  const masteryHTML = Object.entries(data.mastery || {}).map(([concept, value]) => `
    <div style="margin: 5px 0;">
      <strong>${concept}</strong>: ${Math.round(value)}%
    </div>
  `).join('')
  
  const riskPercent = Math.round((data.risk_score || 0) * 100)
  const riskColor = riskPercent > 60 ? 'red' : riskPercent > 30 ? 'orange' : 'green'
  
  container.innerHTML = `
    <button id="backBtn" class="glass-btn" style="margin-bottom:20px;">Back to Students</button>
    
    <div class="glass-panel">
      <h2>Student Dashboard (ID: ${studentId})</h2>
      
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
        <div>
          <h3>Concept Mastery</h3>
          ${masteryHTML}
        </div>
        
        <div>
          <h3>Risk Assessment</h3>
          <p style="font-size: 24px; color: ${riskColor};">
            <strong>${riskPercent}%</strong>
          </p>
          <p>Risk Level: <strong style="color: ${riskColor};">${data.risk_score > 0.6 ? 'HIGH' : data.risk_score > 0.3 ? 'MEDIUM' : 'LOW'}</strong></p>
          ${data.insights?.weak_topics ? `
            <p><strong>Weak Topics:</strong> ${data.insights.weak_topics.join(', ')}</p>
          ` : ''}
        </div>
      </div>
    </div>
  `
  
  document.getElementById('backBtn').addEventListener('click', () => {
    // Show other sections again
    document.getElementById('testsContent').style.display = 'block'
    document.getElementById('studentsContent').style.display = 'block'
    // Refresh enrolled students with fresh data
    renderEnrolledStudents(classroomId)
  })
}