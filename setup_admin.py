#!/usr/bin/env python3
"""
Quick setup script to initialize admin user for testing Admin Dashboard
"""

import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.database import SessionLocal, init_db, engine
from backend.models import User, Base
from backend.auth import get_password_hash

def setup_admin_user():
    """Create an admin user for testing"""
    
    # Initialize database
    print("🔄 Initializing database...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized")
    
    # Create session
    db = SessionLocal()
    
    try:
        # Check if admin already exists
        admin = db.query(User).filter(User.email == "admin@test.com").first()
        if admin:
            print("⚠️  Admin user already exists")
            return
        
        # Create admin user
        admin_user = User(
            email="admin@test.com",
            name="Admin User",
            hashed_password=get_password_hash("admin123"),
            role="admin",
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✅ Admin user created successfully!")
        print(f"   Email: admin@test.com")
        print(f"   Password: admin123")
        print(f"   ID: {admin_user.id}")
        
        # Create some test student users
        print("\n🔄 Creating test student users...")
        
        test_students = [
            ("john_doe@test.com", "John Doe"),
            ("jane_smith@test.com", "Jane Smith"),
            ("bob_wilson@test.com", "Bob Wilson"),
            ("alice_johnson@test.com", "Alice Johnson"),
        ]
        
        for email, name in test_students:
            student = User(
                email=email,
                name=name,
                hashed_password=get_password_hash("password123"),
                role="student",
                is_active=True
            )
            db.add(student)
        
        db.commit()
        print(f"✅ Created {len(test_students)} test students")
        
        print("\n📝 Setup Complete!")
        print("\n📋 Test Credentials:")
        print("   Admin: admin@test.com / admin123")
        print("   Student: john_doe@test.com / password123")
        print("\n🚀 Next steps:")
        print("   1. Start backend: cd backend && python main.py")
        print("   2. Start frontend: cd frontend && npm run dev")
        print("   3. Login at http://localhost:3000/login")
        print("   4. View admin dashboard at http://localhost:3000/admin")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    setup_admin_user()
