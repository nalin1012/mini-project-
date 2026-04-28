"""Firebase Admin SDK Configuration - Optional"""
import os
import json
from typing import Optional, Dict, Any

# Try to import Firebase admin SDK (optional)
try:
    import firebase_admin
    from firebase_admin import credentials, auth, db
    FIREBASE_SDK_AVAILABLE = True
except ImportError:
    FIREBASE_SDK_AVAILABLE = False
    print("⚠️  firebase-admin not installed. Firebase auth will be disabled. Install with: pip install firebase-admin")

def initialize_firebase():
    """Initialize Firebase Admin SDK (optional)"""
    if not FIREBASE_SDK_AVAILABLE:
        print("ℹ️  Firebase Admin SDK not available. Using JWT auth only.")
        return False
    
    try:
        # Try loading from environment variable first
        creds_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
        database_url = os.getenv("FIREBASE_DATABASE_URL")
        
        if creds_json:
            creds_dict = json.loads(creds_json)
            creds = credentials.Certificate(creds_dict)
        else:
            # Try loading from file
            service_account_path = os.path.join(os.path.dirname(__file__), "service-account-key.json")
            if os.path.exists(service_account_path):
                creds = credentials.Certificate(service_account_path)
            else:
                # If no Firebase credentials found, return None (will use JWT auth only)
                print("⚠️  Firebase credentials not found. Using JWT auth only.")
                return False
        
        # Initialize Firebase with database URL if available
        options = {
            'credentials': creds,
        }
        if database_url:
            options['databaseURL'] = database_url
        
        firebase_admin.initialize_app(creds, options)
        print("✓ Firebase Admin SDK initialized successfully")
        return True
    except Exception as e:
        print(f"⚠️  Firebase initialization warning: {str(e)}")
        return False

def verify_firebase_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify Firebase ID token"""
    if not FIREBASE_SDK_AVAILABLE or not FIREBASE_AVAILABLE:
        return None
    
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        print(f"Firebase token verification failed: {str(e)}")
        return None

def get_user_by_firebase_uid(uid: str) -> Optional[Dict[str, Any]]:
    """Get user by Firebase UID"""
    if not FIREBASE_SDK_AVAILABLE or not FIREBASE_AVAILABLE:
        return None
    
    try:
        user = auth.get_user(uid)
        return {
            "uid": user.uid,
            "email": user.email,
            "name": user.display_name or user.email,
            "email_verified": user.email_verified,
        }
    except Exception as e:
        print(f"Firebase get user failed: {str(e)}")
        return None

# Firebase Realtime Database operations
def save_user_progress_to_firebase(user_id: int, progress_data: Dict[str, Any]):
    """Save user progress to Firebase Realtime Database"""
    if not FIREBASE_SDK_AVAILABLE or not FIREBASE_AVAILABLE:
        return False
    
    try:
        ref = db.reference(f"users/{user_id}/progress")
        ref.set(progress_data)
        return True
    except Exception as e:
        print(f"Firebase save progress failed: {str(e)}")
        return False

def get_user_progress_from_firebase(user_id: int) -> Optional[Dict[str, Any]]:
    """Get user progress from Firebase Realtime Database"""
    if not FIREBASE_SDK_AVAILABLE or not FIREBASE_AVAILABLE:
        return None
    
    try:
        ref = db.reference(f"users/{user_id}/progress")
        data = ref.get()
        return data.val() if data else None
    except Exception as e:
        print(f"Firebase get progress failed: {str(e)}")
        return None

def save_quiz_result_to_firebase(user_id: int, quiz_id: str, result_data: Dict[str, Any]):
    """Save quiz result to Firebase Realtime Database"""
    if not FIREBASE_SDK_AVAILABLE or not FIREBASE_AVAILABLE:
        return False
    
    try:
        ref = db.reference(f"users/{user_id}/quiz_results/{quiz_id}")
        ref.set(result_data)
        return True
    except Exception as e:
        print(f"Firebase save quiz result failed: {str(e)}")
        return False

def get_user_quiz_results_from_firebase(user_id: int) -> Optional[Dict[str, Any]]:
    """Get user's quiz results from Firebase Realtime Database"""
    if not FIREBASE_SDK_AVAILABLE or not FIREBASE_AVAILABLE:
        return None
    
    try:
        ref = db.reference(f"users/{user_id}/quiz_results")
        data = ref.get()
        return data.val() if data else {}
    except Exception as e:
        print(f"Firebase get quiz results failed: {str(e)}")
        return None

# Initialize on module import
FIREBASE_AVAILABLE = initialize_firebase()
