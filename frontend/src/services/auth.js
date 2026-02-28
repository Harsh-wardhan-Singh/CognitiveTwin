import { 
  getCurrentUser, 
  loginUser as apiLogin, 
  logoutUser as apiLogout,
  registerUser as apiRegister 
} from './api.js'

/**
 * Check if user has a valid backend session (auth cookie)
 */
export async function checkExistingSession() {
  try {
    const user = await getCurrentUser()
    if (user && user.id) {
      return {
        role: user.role,
        id: user.id,
        email: user.email,
        hasTakenQuiz: user.has_taken_diagnostic || false
      }
    }
  } catch (error) {
    console.log("No valid session found")
  }
  return null
}

/**
 * Register a new user with backend
 */
export async function register(email, password, role) {
  try {
    const response = await apiRegister(email, password, role)
    
    // After successful registration, automatically log in
    await apiLogin(email, password)
    
    // Get the user data
    const user = await getCurrentUser()
    if (user && user.id) {
      return {
        role: user.role,
        id: user.id,
        email: user.email,
        hasTakenQuiz: user.has_taken_diagnostic || false,
        isBackendAuth: true
      }
    }
  } catch (error) {
    console.error("Registration failed:", error)
    
    // Create a detailed error object
    const err = new Error(error.message || "Registration failed")
    err.details = error.details || null
    err.statusCode = error.statusCode || 500
    throw err
  }
}

/**
 * Login with backend authentication
 * No demo credentials - uses real backend only
 */
export async function login(email, password, role) {
  try {
    await apiLogin(email, password)
    
    // After successful backend login, get the user data
    const user = await getCurrentUser()
    if (user && user.id) {
      return {
        role: user.role,
        id: user.id,
        email: user.email,
        hasTakenQuiz: user.has_taken_diagnostic || false,
        isBackendAuth: true
      }
    }
  } catch (error) {
    console.error("Login failed:", error)
    
    // Create a detailed error object
    const err = new Error(error.message || "Invalid credentials")
    err.details = error.details || null
    err.statusCode = error.statusCode || 401
    throw err
  }
}

/**
 * Logout user
 */
export async function logout() {
  try {
    await apiLogout()
  } catch (error) {
    console.error("Logout error:", error)
  }
}
