/* =====================================================
   API SERVICE LAYER
   ===================================================== */

export const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

/**
 * Fetch student dashboard with mastery, risk, and insights
 */
export async function fetchStudentDashboard() {
  try {
    const response = await fetch(`${API_BASE_URL}/student/dashboard`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      credentials: "include"
    })
    
    if (!response.ok) {
      throw new Error(`Failed to fetch dashboard: ${response.statusText}`)
    }
    
    const data = await response.json()
    return data
  } catch (error) {
    console.error("Dashboard fetch error:", error)
    throw error
  }
}

/**
 * Fetch next question for quiz
 */
export async function fetchNextQuestion() {
  try {
    const response = await fetch(`${API_BASE_URL}/quiz/next-question`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      credentials: "include"
    })
    
    if (!response.ok) {
      throw new Error(`Failed to fetch question: ${response.statusText}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error("Question fetch error:", error)
    throw error
  }
}

/**
 * Submit quiz answer and get updated state
 */
export async function submitQuizAnswer(questionId, userAnswer, confidence, responseTime) {
  try {
    const response = await fetch(`${API_BASE_URL}/quiz/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({
        question_id: questionId,
        user_answer: userAnswer,
        confidence: confidence,
        response_time: responseTime
      })
    })
    
    if (!response.ok) {
      throw new Error(`Failed to submit answer: ${response.statusText}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error("Answer submission error:", error)
    throw error
  }
}

/**
 * Get current risk score
 */
export async function fetchRiskScore() {
  try {
    const response = await fetch(`${API_BASE_URL}/quiz/risk-score`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      credentials: "include"
    })
    
    if (!response.ok) {
      throw new Error(`Failed to fetch risk score: ${response.statusText}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error("Risk score fetch error:", error)
    throw error
  }
}

/**
 * Get explanation for a question (AI-generated)
 */
export async function fetchExplanation(questionId) {
  try {
    const response = await fetch(`${API_BASE_URL}/quiz/explanation/${questionId}`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      credentials: "include"
    })
    
    if (!response.ok) {
      throw new Error(`Failed to fetch explanation: ${response.statusText}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error("Explanation fetch error:", error)
    throw error
  }
}

/**
 * Fetch class insights (teacher only)
 */
export async function fetchClassInsights(classroomId) {
  try {
    const response = await fetch(`${API_BASE_URL}/teacher/classroom/${classroomId}/insights`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      credentials: "include"
    })
    
    if (!response.ok) {
      throw new Error(`Failed to fetch class insights: ${response.statusText}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error("Class insights fetch error:", error)
    throw error
  }
}

/**
 * Fetch a specific student's dashboard (teacher view)
 */
export async function fetchStudentDashboardTeacherView(studentId) {
  try {
    const response = await fetch(`${API_BASE_URL}/teacher/student/${studentId}/dashboard`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      credentials: "include"
    })
    
    if (!response.ok) {
      throw new Error(`Failed to fetch student dashboard: ${response.statusText}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error("Student dashboard fetch error:", error)
    throw error
  }
}

/**
 * Get student's enrolled classrooms
 */
export async function fetchStudentClassrooms() {
  try {
    const response = await fetch(`${API_BASE_URL}/student/classrooms`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      credentials: "include"
    })
    
    if (!response.ok) {
      throw new Error(`Failed to fetch classrooms: ${response.statusText}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error("Classrooms fetch error:", error)
    throw error
  }
}

/**
 * Join a classroom by ID
 */
export async function joinClassroom(classroomId) {
  try {
    const response = await fetch(`${API_BASE_URL}/student/join/${classroomId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include"
    })
    
    if (!response.ok) {
      throw new Error(`Failed to join classroom: ${response.statusText}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error("Classroom join error:", error)
    throw error
  }
}

/**
 * Login user
 */
export async function loginUser(email, password) {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({
        email: email,
        password: password
      })
    })
    
    const data = await response.json()
    
    if (!response.ok) {
      const error = new Error(data.message || data.detail || `Login failed: ${response.statusText}`)
      error.statusCode = response.status
      error.details = data.details || null
      throw error
    }
    
    return data
  } catch (error) {
    console.error("Login error:", error)
    throw error
  }
}

/**
 * Register new user
 */
export async function registerUser(email, password, role) {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: email,
        password: password,
        role: role
      })
    })
    
    const data = await response.json()
    
    if (!response.ok) {
      const error = new Error(data.message || data.detail || `Registration failed: ${response.statusText}`)
      error.statusCode = response.status
      error.details = data.details || null
      throw error
    }
    
    return data
  } catch (error) {
    console.error("Registration error:", error)
    throw error
  }
}

/**
 * Get current logged-in user
 */
export async function getCurrentUser() {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/me`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      credentials: "include"
    })
    
    const data = await response.json()
    
    if (!response.ok) {
      const error = new Error(data.message || data.detail || `Failed to fetch user: ${response.statusText}`)
      error.statusCode = response.status
      error.details = data.details || null
      throw error
    }
    
    return data
  } catch (error) {
    console.error("Current user fetch error:", error)
    throw error
  }
}

/**
 * Logout user
 */
export async function logoutUser() {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/logout`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include"
    })
    
    const data = await response.json()
    
    if (!response.ok) {
      const error = new Error(data.message || data.detail || `Logout failed: ${response.statusText}`)
      error.statusCode = response.status
      error.details = data.details || null
      throw error
    }
    
    return data
  } catch (error) {
    console.error("Logout error:", error)
    throw error
  }
}

/**
 * Fetch all questions grouped by concept
 */
export async function fetchAllQuestions() {
  try {
    const response = await fetch(`${API_BASE_URL}/quiz/questions/all`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      credentials: "include"
    })
    
    if (!response.ok) {
      throw new Error(`Failed to fetch all questions: ${response.statusText}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error("All questions fetch error:", error)
    throw error
  }
}

/**
 * Fetch questions for a specific concept
 */
export async function fetchQuestionsByConcept(concept) {
  try {
    const response = await fetch(`${API_BASE_URL}/quiz/questions/by-concept/${concept}`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      credentials: "include"
    })
    
    if (!response.ok) {
      throw new Error(`Failed to fetch questions for concept: ${response.statusText}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error("Concept questions fetch error:", error)
    throw error
  }
}

/**
 * Check if user has attempted the quiz
 */
export async function checkHasAttemptedQuiz() {
  try {
    const response = await fetch(`${API_BASE_URL}/quiz/has-attempted`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      credentials: "include"
    })
    
    if (!response.ok) {
      throw new Error(`Failed to check quiz attempt status: ${response.statusText}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error("Quiz attempt check error:", error)
    throw error
  }
}

/**
 * Get teacher's classrooms
 */
export async function fetchTeacherClassrooms() {
  try {
    const response = await fetch(`${API_BASE_URL}/teacher/classrooms`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      credentials: "include"
    })
    
    if (!response.ok) {
      throw new Error(`Failed to fetch teacher classrooms: ${response.statusText}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error("Teacher classrooms fetch error:", error)
    throw error
  }
}

/**
 * Get students in a classroom
 */
export async function fetchClassroomStudents(classroomId) {
  try {
    const response = await fetch(`${API_BASE_URL}/teacher/classroom/${classroomId}/students`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      credentials: "include"
    })
    
    if (!response.ok) {
      throw new Error(`Failed to fetch classroom students: ${response.statusText}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error("Classroom students fetch error:", error)
    throw error
  }
}

/**
 * Create a classroom
 */
export async function createTeacherClassroom(name) {
  try {
    const response = await fetch(`${API_BASE_URL}/teacher/classroom`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({
        name: name,
        subject: "",
        syllabus_scope: "",
        exam_pattern: "",
        progress_topics: []
      })
    })
    
    if (!response.ok) {
      throw new Error(`Failed to create classroom: ${response.statusText}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error("Create classroom error:", error)
    throw error
  }
}
