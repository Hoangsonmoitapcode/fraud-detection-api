from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Database Configuration
# Priority: Environment Variable > Local Default
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+psycopg2://fastapi_user:mypassword@localhost:5432/fastapi_db"
)

# Connection Configuration
engine = create_engine(
    DATABASE_URL,
    # Connection pool settings (good for both local and remote)
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,  # Recycle connections every hour
    echo=False  # Set to True for SQL debugging
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Test connection function
def test_connection():
    """Test database connection"""
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✅ Database connection successful!")
            print(f"📊 Connected to: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'localhost'}")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print(f"🔧 Connection string: {DATABASE_URL.split('://')[0]}://***@{DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'localhost'}")
        return False
