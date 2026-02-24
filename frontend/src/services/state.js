let studentState = {
  mastery: {
    Binomial: 70,
    Poisson: 65,
    Normal: 72,
    Bayes: 60,
    Conditional: 75
  },
  risk: 40
}

const conceptGraph = {
  Conditional: ["Bayes"],
  Bayes: [],
  Binomial: ["Normal"],
  Normal: [],
  Poisson: []
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

export function updateCognitiveMastery(concept, correct, signal) {
  const current = studentState.mastery[concept]

  let delta

  if (correct) {
    delta = 10 * signal
    studentState.mastery[concept] = Math.min(100, current + delta)
  } else {
    delta = -12 * signal
    studentState.mastery[concept] = Math.max(10, current + delta)
  }

  // Dependency propagation
  const relatedConcepts = conceptGraph[concept] || []

  relatedConcepts.forEach(related => {
    const relatedCurrent = studentState.mastery[related]

    // Apply smaller ripple effect (30% of delta)
    const propagatedChange = delta * 0.3

    studentState.mastery[related] = Math.max(
      10,
      Math.min(100, relatedCurrent + propagatedChange)
    )
  })
}