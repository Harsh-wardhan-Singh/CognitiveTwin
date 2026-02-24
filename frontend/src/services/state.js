let studentState = {
  mastery: [80, 65, 72, 60, 75],
  risk: 38
}

export function getStudentState() {
  return studentState
}

export function updateStudentState(newState) {
  studentState = {
    ...studentState,
    ...newState
  }
}