const STORAGE_KEY = 'cognitive_twin_tests'

function load() {
  const data = localStorage.getItem(STORAGE_KEY)
  return data ? JSON.parse(data) : []
}

function save(tests) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(tests))
}

export function createTest({
  classroomId,
  topic,
  difficulty,
  numQuestions
}) {
  const tests = load()

  const id =
    "T" + Math.random().toString(36).substring(2, 8)

  const test = {
    id,
    classroomId,
    topic,
    difficulty,
    numQuestions,
    createdAt: Date.now()
  }

  tests.push(test)
  save(tests)

  return test
}

export function getTestsForClassroom(classroomId) {
  const tests = load()
  return tests.filter(
    t => t.classroomId === classroomId
  )
}