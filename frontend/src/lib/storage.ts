/**
 * Legacy student-id helpers kept for compatibility with future customizations.
 * Authentication and sessions are owned by Supabase Auth.
 */
const KEY = 'skillsensei_student_id'
export const getStudentId = () => localStorage.getItem(KEY)
export const setStudentId = (id: string) => localStorage.setItem(KEY, id)
export const clearStudentId = () => localStorage.removeItem(KEY)
