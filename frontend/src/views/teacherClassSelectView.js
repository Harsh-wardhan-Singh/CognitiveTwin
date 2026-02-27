import { createTeacherClassroom, fetchTeacherClassrooms } from '../services/api.js'
import { currentUser, mountView } from '../testApp.js'
import { renderTeacherClassView } from './teacherClassView.js'

export async function renderTeacherClassSelect() {

  mountView((container) => {

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

    // Fetch classrooms from backend
    fetchTeacherClassrooms().then(classrooms => {
      if (classrooms.length === 0) {
        classList.innerHTML = `<p>No classrooms yet.</p>`
      } else {
        classList.innerHTML = classrooms.map(c => `
          <div class="glass-panel clickable"
               data-id="${c.id}">
            <strong>${c.name}</strong><br/>
            Subject: ${c.subject || 'N/A'}
          </div>
        `).join('')
        
        // Add click handlers
        container.querySelectorAll('.clickable')
          .forEach(panel => {
            panel.addEventListener('click', () => {
              currentUser.activeClass = panel.dataset.id
              renderTeacherClassView()
            })
          })
      }
    }).catch(err => {
      console.error("Failed to load classrooms:", err)
      classList.innerHTML = `<p>Error loading classrooms</p>`
    })

    container.querySelector('#createClassBtn')
      .addEventListener('click', async () => {
        const name = prompt("Enter classroom name:")
        if (!name) return
        
        try {
          const newClassroom = await createTeacherClassroom(name)
          alert(`Classroom created! Share code: ${newClassroom.id}`)
          renderTeacherClassSelect()
        } catch (err) {
          alert("Failed to create classroom: " + err.message)
        }
      })

  })
}