from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import os
import time
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, database_url=None):
        # Get database credentials from environment variables
        db_user = os.getenv('DB_USER', 'postgres')
        db_password = os.getenv('DB_PASSWORD', 'postgres')
        db_host = os.getenv('DB_HOST', 'db')
        db_name = os.getenv('DB_NAME', 'scenarios_db')
        
        # Construct database URL if not provided
        if not database_url:
            database_url = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
        
        self.database_url = database_url
        
        # Add retry logic for database connection
        max_retries = 5
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                self.engine = create_engine(self.database_url)
                # Test the connection
                self.engine.connect()
                # Create tables
                Base.metadata.create_all(self.engine)
                self.SessionLocal = sessionmaker(bind=self.engine)
                logger.info("Successfully connected to the database")
                break
            except Exception as e:
                retry_count += 1
                if retry_count == max_retries:
                    logger.error(f"Could not connect to database after {max_retries} attempts")
                    raise
                logger.warning(f"Database connection attempt {retry_count} failed, retrying...")
                time.sleep(2)
    
    def get_session(self):
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close() 