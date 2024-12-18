#!/usr/bin/env python
# coding: utf-8

import os
import mysql.connector
import psycopg2
from dotenv import load_dotenv
from typing import Dict, Any

class DatabaseManager:
    """Manages database connections and operations for both MySQL and PostgreSQL"""
    
    def __init__(self):
        load_dotenv()
        self.mysql_config = {
            'host': os.getenv('MYSQL_HOST', 'localhost'),
            'user': os.getenv('MYSQL_USER', 'root'),
            'password': os.getenv('MYSQL_PASSWORD', ''),
            'database': os.getenv('MYSQL_DATABASE', 'group_cases')
        }
        
        self.pg_config = {
            'host': os.getenv('PG_HOST', 'localhost'),
            'user': os.getenv('PG_USER', 'postgres'),
            'password': os.getenv('PG_PASSWORD', ''),
            'database': os.getenv('PG_DATABASE', 'group_cases')
        }
        
    def _create_tables(self, cursor, is_mysql: bool = True):
        """Create necessary tables if they don't exist"""
        if is_mysql:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS discussions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    discussion_type VARCHAR(50),
                    discussion_name VARCHAR(255),
                    context TEXT,
                    metadata JSON,
                    results JSON,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        else:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS discussions (
                    id SERIAL PRIMARY KEY,
                    discussion_type VARCHAR(50),
                    discussion_name VARCHAR(255),
                    context TEXT,
                    metadata JSONB,
                    results JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
    def store_data(self, results: Dict[str, Any], metadata: Dict[str, Any]):
        """Store data in both MySQL and PostgreSQL databases"""
        # Store in MySQL
        try:
            conn = mysql.connector.connect(**self.mysql_config)
            cursor = conn.cursor()
            self._create_tables(cursor, True)
            
            cursor.execute("""
                INSERT INTO discussions 
                (discussion_type, discussion_name, context, metadata, results)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                metadata.get('discussion_type', 'unknown'),
                metadata.get('discussion_name', 'unnamed'),
                metadata.get('context', ''),
                metadata.get('metadata', '{}'),
                str(results)
            ))
            conn.commit()
            
        except Exception as e:
            print(f"MySQL Error: {e}")
        finally:
            if 'conn' in locals():
                conn.close()
                
        # Store in PostgreSQL
        try:
            conn = psycopg2.connect(**self.pg_config)
            cursor = conn.cursor()
            self._create_tables(cursor, False)
            
            cursor.execute("""
                INSERT INTO discussions 
                (discussion_type, discussion_name, context, metadata, results)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                metadata.get('discussion_type', 'unknown'),
                metadata.get('discussion_name', 'unnamed'),
                metadata.get('context', ''),
                metadata.get('metadata', '{}'),
                str(results)
            ))
            conn.commit()
            
        except Exception as e:
            print(f"PostgreSQL Error: {e}")
        finally:
            if 'conn' in locals():
                conn.close()
                
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass  # Connections are handled per operation
