/* ============================= */
/* CLASSROOM STORE (LOCAL STORAGE) */
/* ============================= */

const STORAGE_KEY = 'cognitive_twin_classrooms'

function load() {
  const data = localStorage.getItem(STORAGE_KEY)
  return data ? JSON.parse(data) : []
}

function save(classrooms) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(classrooms))
}

function generateCode() {
  return Math.random().toString(36).substring(2, 8).toUpperCase()
}

export function createClassroom(teacherId) {
  const classrooms = load()

 const classroom = {
  id: generateCode(),
  teacherId,
  students: [],
  testAttempts: []  
}

  classrooms.push(classroom)
  save(classrooms)

  return classroom
}

export function joinClassroom(code, studentId) {
  const classrooms = load()

  const classroom = classrooms.find(c => c.id === code)

  if (!classroom) return null

  if (!classroom.students.includes(studentId)) {
    classroom.students.push(studentId)
  }

  save(classrooms)

  return classroom
}

export function getTeacherClassrooms(teacherId) {
  const classrooms = load()
  return classrooms.filter(c => c.teacherId === teacherId)
}

export function getStudentClassrooms(studentId) {
  const classrooms = load()
  return classrooms.filter(c => c.students.includes(studentId))
}

export function saveTestAttempt(classCode, studentId, attemptData) {
  const classrooms = load()

  const classroom = classrooms.find(c => c.id === classCode)

  if (!classroom) return

  if (!classroom.testAttempts) {
    classroom.testAttempts = []
  }

  classroom.testAttempts.push({
    studentId,
    ...attemptData
  })

  save(classrooms)
}
export function getClassroomById(classCode) {
  const classrooms = load()
  return classrooms.find(c => c.id === classCode)
}