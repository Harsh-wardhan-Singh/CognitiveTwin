import { createClassroom, getTeacherClassrooms } from '../services/classroomStore.js'
import { currentUser, mountView } from '../testApp.js'
import { renderTeacherClassView } from './teacherClassView.js'

export function renderTeacherClassSelect() {

  mountView((container) => {

    const teacherId = currentUser.email
    const classrooms = getTeacherClassrooms(teacherId)

    container.innerHTML = `
      <div class="dashboard-container">
        <h1>Your Classrooms</h1>

        <button id="createClassBtn" class="glass-btn">
          Create New Classroom
        </button>

        <div id="classList" style="margin-top:20px;"></div>
      </div>
    `

    const classList = container.querySelector('#classList')

    if (classrooms.length === 0) {
      classList.innerHTML = `<p>No classrooms yet.</p>`
    } else {
      classList.innerHTML = classrooms.map(c => `
        <div class="glass-panel clickable"
             data-code="${c.id}">
          Classroom Code: ${c.id}
        </div>
      `).join('')
    }

    container.querySelector('#createClassBtn')
      .addEventListener('click', () => {
        const classroom = createClassroom(teacherId)

        alert(
          `Classroom created!\n\nInvite link:\nhttp://localhost:5173/join/${classroom.id}`
        )

        renderTeacherClassSelect()
      })

    container.querySelectorAll('.clickable')
      .forEach(panel => {
        panel.addEventListener('click', () => {
          currentUser.activeClass = panel.dataset.code
          renderTeacherClassView()
        })
      })

  })
}