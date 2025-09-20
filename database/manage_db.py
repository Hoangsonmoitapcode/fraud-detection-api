#!/usr/bin/env python3
"""
Database management script for FraudDetection project
"""
import sys
import os
import subprocess

# Add parent directory to path so we can import from src
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.database import engine
from src.models import Base

def drop_tables():
    """Drop all tables"""
    Base.metadata.drop_all(bind=engine)
    print("✅ All tables dropped successfully")

def create_tables():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully")

def reset_database():
    """Drop and recreate all tables (WARNING: Loses migration history!)"""
    drop_tables()
    create_tables()
    print("✅ Database reset completed")
    print("⚠️  Run 'python -m alembic stamp head' to sync migration history")

def migrate():
    """Apply pending migrations"""
    result = subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"])
    if result.returncode == 0:
        print("✅ Migrations applied successfully")
    else:
        print("❌ Migration failed")

def migration_status():
    """Show current migration status"""
    subprocess.run([sys.executable, "-m", "alembic", "current"])
    subprocess.run([sys.executable, "-m", "alembic", "history", "--verbose"])

def populate_headings():
    """Populate phone headings database"""
    try:
        from src.populate_headings import populate_phone_headings
        populate_phone_headings()
    except ImportError as e:
        print(f"❌ Error importing populate_headings: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python manage_db.py [drop|create|reset|migrate|status|populate]")
        print("  drop     - Drop all tables")
        print("  create   - Create all tables")
        print("  reset    - Drop and recreate tables (loses data!)")
        print("  migrate  - Apply pending migrations")
        print("  status   - Show migration status")
        print("  populate - Populate phone headings database")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "drop":
        drop_tables()
    elif command == "create":
        create_tables()
    elif command == "reset":
        reset_database()
    elif command == "migrate":
        migrate()
    elif command == "status":
        migration_status()
    elif command == "populate":
        populate_headings()
    else:
        print("Invalid command. Use: drop, create, reset, migrate, status, or populate")
        sys.exit(1)
