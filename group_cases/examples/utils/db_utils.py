import os
import json
import mysql.connector
import psycopg2
from dotenv import load_dotenv
from datetime import datetime
from typing import Dict, Any, Optional

# Load environment variables
load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.mysql_conn = None
        self.postgres_conn = None
        self.setup_connections()

    def setup_connections(self):
        """Setup connections to both MySQL and PostgreSQL databases"""
        try:
            self.mysql_conn = mysql.connector.connect(
                host=os.getenv('MYSQL_HOST'),
                user=os.getenv('MYSQL_USER'),
                password=os.getenv('MYSQL_PASSWORD'),
                database=os.getenv('MYSQL_DATABASE')
            )
            
            self.postgres_conn = psycopg2.connect(os.getenv('POSTGRES_URI'))
            
            self._create_tables()
        except Exception as e:
            print(f"Error setting up database connections: {str(e)}")
            raise

    def _create_tables(self):
        """Create necessary tables in both databases"""
        for conn, is_postgres in [(self.mysql_conn, False), (self.postgres_conn, True)]:
            cursor = conn.cursor()
            
            # JSON type varies between MySQL and PostgreSQL
            json_type = "JSONB" if is_postgres else "JSON"
            id_type = "SERIAL" if is_postgres else "INT AUTO_INCREMENT"
            
            tables = [
                f"""
                CREATE TABLE IF NOT EXISTS agent_insights (
                    id {id_type} PRIMARY KEY,
                    agent_name VARCHAR(255),
                    main_point TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """,
                f"""
                CREATE TABLE IF NOT EXISTS agent_usecases (
                    id {id_type} PRIMARY KEY,
                    agent_name VARCHAR(255),
                    usecase_type VARCHAR(255),
                    content TEXT,
                    metadata {json_type},
                    source VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            ]
            
            for table_sql in tables:
                cursor.execute(table_sql)
            
            conn.commit()
            cursor.close()

    def store_agent_data(self, 
                        extraction_data: Dict[str, Any],
                        usecase_type: str = 'rental_ad',
                        metadata: Optional[Dict[str, Any]] = None):
        """
        Store agent data in both databases
        
        Args:
            extraction_data: Dictionary containing agent extractions and world extraction
            usecase_type: Type of use case (default: 'rental_ad')
            metadata: Additional metadata for the use case
        """
        try:
            # Store in MySQL
            self._store_in_database(self.mysql_conn, extraction_data, usecase_type, metadata)
            
            # Store in PostgreSQL
            self._store_in_database(self.postgres_conn, extraction_data, usecase_type, metadata)
            
            print("Data successfully stored in both databases!")
        except Exception as e:
            print(f"Error storing data: {str(e)}")
            raise

    def _store_in_database(self, conn, extraction_data: Dict[str, Any], usecase_type: str, metadata: Optional[Dict[str, Any]]):
        """Store data in a specific database"""
        cursor = conn.cursor()
        
        try:
            # Store agent insights
            for agent_name, insights in extraction_data.get('agent_extractions', {}).items():
                for insight in insights:
                    cursor.execute(
                        'INSERT INTO agent_insights (agent_name, main_point) VALUES (%s, %s)',
                        (agent_name, insight.get('main_point'))
                    )
            
            # Store usecase data
            world_extraction = extraction_data.get('world_extraction', {})
            if world_extraction:
                for source, content in world_extraction.items():
                    if isinstance(content, dict) and 'ad_copy' in content:
                        cursor.execute(
                            '''INSERT INTO agent_usecases 
                               (agent_name, usecase_type, content, metadata, source) 
                               VALUES (%s, %s, %s, %s, %s)''',
                            ('group', usecase_type, content['ad_copy'], 
                             json.dumps(metadata) if metadata else None, source)
                        )
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    def close_connections(self):
        """Close all database connections"""
        if self.mysql_conn:
            self.mysql_conn.close()
        if self.postgres_conn:
            self.postgres_conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connections()
