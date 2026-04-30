#!/usr/bin/env python3
"""
Safely add an admin user to the production database without dropping tables.

Usage:
  python add_admin.py --email admin@example.com --password Secret123 --name "Admin Name"

Run this from the backend directory or via your host's shell (Render shell).
This will check for existing user by email and create one if missing.
"""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, init_db
from models import User
from auth import get_password_hash


def add_admin(email: str, password: str, name: str = "Admin"):
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print(f"User with email {email} already exists (id={existing.id}, role={existing.role})")
            if existing.role != 'admin':
                existing.role = 'admin'
                existing.is_active = True
                db.add(existing)
                db.commit()
                print("Upgraded existing user to admin.")
            return

        hashed = get_password_hash(password)
        user = User(
            email=email,
            name=name,
            hashed_password=hashed,
            role="admin",
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print("Admin user created:")
        print(f"  id: {user.id}")
        print(f"  email: {user.email}")
        print(f"  password: (the value you provided)")
    except Exception as e:
        print(f"Error creating admin: {e}")
        db.rollback()
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description="Add or upgrade an admin user")
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--name", default="Admin")
    args = parser.parse_args()

    # Ensure DB is initialized (idempotent)
    try:
        init_db()
    except Exception:
        pass

    add_admin(args.email, args.password, args.name)


if __name__ == "__main__":
    main()
