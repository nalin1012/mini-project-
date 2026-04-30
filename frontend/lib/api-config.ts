/**
 * API Configuration
 * Centralized location for API base URL and configuration
 * Used across all components to ensure consistency
 */

export const API_CONFIG = {
  BASE_URL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001",
  ENVIRONMENT: process.env.NEXT_PUBLIC_ENVIRONMENT || "development",
  APP_NAME: process.env.NEXT_PUBLIC_APP_NAME || "AI Learning Platform",
};

/**
 * Build a full API endpoint URL
 * @param endpoint - The API endpoint (e.g., "/api/auth/login")
 * @returns Full URL
 */
export const getApiUrl = (endpoint: string): string => {
  const baseUrl = API_CONFIG.BASE_URL.endsWith("/") 
    ? API_CONFIG.BASE_URL.slice(0, -1) 
    : API_CONFIG.BASE_URL;
  
  const path = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
  return `${baseUrl}${path}`;
};

/**
 * Make an API request with error handling
 * @param endpoint - API endpoint
 * @param options - Fetch options
 * @returns Response data or error
 */
export const apiCall = async (
  endpoint: string,
  options: RequestInit = {}
): Promise<any> => {
  try {
    const url = getApiUrl(endpoint);
    
    // Add authorization token if it exists
    const headers = {
      "Content-Type": "application/json",
      ...options.headers,
    };
    
    const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }
    
    const response = await fetch(url, {
      ...options,
      headers,
    });
    
    if (!response.ok) {
      // Handle 401 Unauthorized - redirect to login
      if (response.status === 401) {
        if (typeof window !== "undefined") {
          localStorage.removeItem("access_token");
          localStorage.removeItem("user");
          window.location.href = "/login";
        }
      }
      
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.detail || errorData.message || `API Error: ${response.status}`
      );
    }
    
    return await response.json();
  } catch (error) {
    console.error(`API Error [${endpoint}]:`, error);
    throw error;
  }
};

export default API_CONFIG;
