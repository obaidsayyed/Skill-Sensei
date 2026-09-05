/**
 * Legacy storage helpers kept for compatibility with any future customizations.
 * Authentication and session state are now owned by Clerk.
 */
const KEY = 'skillsensei_student_id'
export const getStudentId = () => localStorage.getItem(KEY)
export const setStudentId = (id: string) => localStorage.setItem(KEY, id)
export const clearStudentId = () => localStorage.removeItem(KEY)
