/**
 * Error Handling Utilities
 * Provides consistent error handling across the application
 */

export class APIError extends Error {
  constructor(
    public status: number,
    public message: string,
    public details?: any
  ) {
    super(message);
    this.name = "APIError";
  }
}

export class NetworkError extends Error {
  constructor(message: string = "Network connection failed") {
    super(message);
    this.name = "NetworkError";
  }
}

export class ValidationError extends Error {
  constructor(
    public message: string,
    public fields?: Record<string, string>
  ) {
    super(message);
    this.name = "ValidationError";
  }
}

/**
 * Parse and format API error messages
 */
export const formatErrorMessage = (error: any): string => {
  if (error instanceof APIError) {
    return error.message;
  }

  if (error instanceof NetworkError) {
    return "Unable to connect to server. Please check your internet connection.";
  }

  if (error instanceof ValidationError) {
    return error.message;
  }

  if (error?.response?.data?.detail) {
    const detail = error.response.data.detail;
    if (typeof detail === "string") {
      return detail;
    }
    if (Array.isArray(detail) && detail.length > 0) {
      return detail[0].msg || detail[0].message || "Validation error";
    }
  }

  if (error instanceof TypeError) {
    if (error.message.includes("fetch")) {
      return "Network connection failed. Please check your internet connection.";
    }
  }

  if (error instanceof Error) {
    return error.message;
  }

  return "An unexpected error occurred. Please try again.";
};

/**
 * Handle API errors and return formatted message
 */
export const handleApiError = (error: any): { message: string; fields?: Record<string, string> } => {
  if (error instanceof ValidationError) {
    return {
      message: error.message,
      fields: error.fields,
    };
  }

  return {
    message: formatErrorMessage(error),
  };
};

/**
 * Determine if error is recoverable
 */
export const isRecoverableError = (error: any): boolean => {
  // Network errors are usually recoverable (retry)
  if (error instanceof NetworkError) return true;

  // 5xx errors are usually recoverable (retry)
  if (error instanceof APIError && error.status >= 500) return true;

  // 429 (Too Many Requests) is recoverable (rate limit)
  if (error instanceof APIError && error.status === 429) return true;

  // 401/403 are not recoverable in the normal sense (user needs to log in)
  if (error instanceof APIError && (error.status === 401 || error.status === 403)) return false;

  // 4xx validation errors are not recoverable
  if (error instanceof APIError && error.status >= 400 && error.status < 500) return false;

  return false;
};

/**
 * Retry logic for API calls
 */
export const withRetry = async <T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  delayMs: number = 1000
): Promise<T> => {
  let lastError: any;

  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;

      if (!isRecoverableError(error)) {
        throw error;
      }

      // Wait before retrying
      if (i < maxRetries - 1) {
        await new Promise((resolve) => setTimeout(resolve, delayMs * Math.pow(2, i)));
      }
    }
  }

  throw lastError;
};

export default {
  APIError,
  NetworkError,
  ValidationError,
  formatErrorMessage,
  handleApiError,
  isRecoverableError,
  withRetry,
};
