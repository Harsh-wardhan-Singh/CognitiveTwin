import { renderTeacherClassView } from './teacherClassView.js'

export function renderTeacherClassSelect() {
  const app = document.getElementById('app')

  app.innerHTML = `
    <div class="dashboard-container">
      <h1>Select Classroom</h1>

      <div class="class-card" id="class1">
        <h2>Probability & Statistics - Section A</h2>
        <p>20 Students</p>
      </div>
    </div>
  `

  document.getElementById('class1')
    .addEventListener('click', () => {
      renderTeacherClassView()
    })
}