/* ============================= */
/* STUDENT STATE */
/* ============================= */

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

/* ============================= */
/* CONCEPT DEPENDENCY GRAPH */
/* ============================= */

const conceptGraph = {
  Conditional: ["Bayes"],
  Bayes: [],
  Binomial: ["Normal"],
  Normal: [],
  Poisson: []
}

/* ============================= */
/* MOMENTUM TRACKING */
/* ============================= */

let masteryMomentum = {}

Object.keys(studentState.mastery).forEach(concept => {
  masteryMomentum[concept] = 0
})

/* ============================= */
/* STATE GETTERS / SETTERS */
/* ============================= */

export function getStudentState() {
  return studentState
}

export function updateStudentState(newState) {
  studentState = {
    ...studentState,
    ...newState
  }
}

/* ============================= */
/* COGNITIVE MASTERY ENGINE */
/* ============================= */

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

  // Track momentum
  masteryMomentum[concept] = delta

  /* 🔥 Dependency propagation */
  const relatedConcepts = conceptGraph[concept] || []

  relatedConcepts.forEach(related => {
    const relatedCurrent = studentState.mastery[related]

    const propagatedChange = delta * 0.3

    studentState.mastery[related] = Math.max(
      10,
      Math.min(100, relatedCurrent + propagatedChange)
    )
  })
}

/* ============================= */
/* ADVANCED RISK ENGINE */
/* ============================= */

export function calculateRisk() {
  const masteryValues = Object.values(studentState.mastery)

  const weakest = Math.min(...masteryValues)

  const avg =
    masteryValues.reduce((a, b) => a + b, 0) / masteryValues.length

  const variance =
    masteryValues.reduce(
      (sum, val) => sum + Math.pow(val - avg, 2),
      0
    ) / masteryValues.length

  const volatility =
    Object.values(masteryMomentum)
      .filter(v => v < 0)
      .reduce((sum, v) => sum + Math.abs(v), 0)

  const riskScore =
    0.4 * (100 - weakest) +
    0.3 * variance +
    0.3 * volatility

  return Math.min(100, Math.max(5, riskScore))
}