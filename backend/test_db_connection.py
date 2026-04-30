#!/usr/bin/env python3
"""
Database Connection Test Script
Run this to verify your database configuration before deploying to Render
"""

import os
import sys
from dotenv import load_dotenv

# Load .env file
load_dotenv()

print("=" * 60)
print("DATABASE CONNECTION TEST")
print("=" * 60)

# Get DATABASE_URL
database_url = os.getenv("DATABASE_URL", "sqlite:///./learning_platform.db")

print(f"\n1️⃣  DATABASE_URL Check:")
print(f"   Value: {database_url[:50]}..." if len(database_url) > 50 else f"   Value: {database_url}")

if not database_url or database_url.strip() == "":
    print("   ❌ ERROR: DATABASE_URL is empty!")
    print("   💡 Set it in your .env file or Render dashboard")
    sys.exit(1)

if "host" in database_url and "postgresql" in database_url:
    if "@" not in database_url:
        print("   ❌ ERROR: Invalid PostgreSQL format (missing @)")
        print("   💡 Should be: postgresql://user:password@hostname:port/dbname")
        sys.exit(1)

print("   ✅ DATABASE_URL format looks good")

# Check if PostgreSQL or SQLite
is_postgresql = "postgresql" in database_url
db_type = "PostgreSQL" if is_postgresql else "SQLite"

print(f"\n2️⃣  Database Type: {db_type}")

# Try to import and test connection
print(f"\n3️⃣  Testing Connection...")

try:
    from sqlalchemy import create_engine, text
    print("   ✅ SQLAlchemy imported")
    
    # Prepare URL
    test_url = database_url
    if is_postgresql and test_url.startswith("postgresql://"):
        test_url = test_url.replace("postgresql://", "postgresql+psycopg://", 1)
    
    # Create engine
    print(f"   Creating engine...")
    if "sqlite" in test_url:
        engine = create_engine(test_url, connect_args={"check_same_thread": False})
    else:
        engine = create_engine(test_url, pool_pre_ping=True)
    
    print("   ✅ Engine created")
    
    # Test connection
    print(f"   Testing {db_type} connection...")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        result.close()
    
    print(f"   ✅ Connection successful!")
    
except Exception as e:
    print(f"   ❌ Connection failed: {str(e)}")
    print(f"\n   Troubleshooting:")
    if is_postgresql:
        print(f"   - Verify PostgreSQL database is running")
        print(f"   - Check hostname is correct")
        print(f"   - Verify username and password")
        print(f"   - Confirm database exists")
        print(f"   - For Render: Use 'Internal Database URL' not 'External'")
    else:
        print(f"   - Check file permissions")
        print(f"   - Verify path is correct")
    sys.exit(1)

# Test models
print(f"\n4️⃣  Testing Models...")

try:
    from database import Base, init_db
    print("   ✅ Database module imported")
    
    init_db()
    print("   ✅ Tables initialized")
    
except Exception as e:
    print(f"   ❌ Model test failed: {str(e)}")
    sys.exit(1)

# All tests passed
print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print("\n🚀 Your database is ready for deployment!\n")

print("Next steps:")
if is_postgresql:
    print("1. If deploying to Render:")
    print("   - Go to Render Dashboard")
    print("   - Set DATABASE_URL in Environment Variables")
    print("   - Use the 'Internal Database URL' from your PostgreSQL service")
    print("   - Click 'Manual Deploy'")
else:
    print("1. SQLite is configured for local development")
    print("2. For production, set up PostgreSQL and update DATABASE_URL")

print("\nFor any issues, check:")
print("- RENDER_DEPLOYMENT_CRITICAL.md (deployment guide)")
print("- AUDIT_REPORT.md (technical details)")
