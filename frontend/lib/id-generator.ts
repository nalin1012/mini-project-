/**
 * Safe ID/UUID generator that works in all environments
 * Tries crypto.randomUUID first, falls back to timestamp + random
 */

export function generateId(): string {
  // Try using crypto.randomUUID if available
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    try {
      return crypto.randomUUID()
    } catch (e) {
      // Fall through to fallback
    }
  }

  // Fallback: Use timestamp + random number
  // Format: timestamp(13 digits) + random(8 digits) = unique enough for client-side
  const timestamp = Date.now().toString(36)
  const randomNum = Math.random().toString(36).substring(2, 10)
  return `${timestamp}-${randomNum}`
}

/**
 * Generate a session ID
 */
export function generateSessionId(): string {
  return `session-${generateId()}`
}
