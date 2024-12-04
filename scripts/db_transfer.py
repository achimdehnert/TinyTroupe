import os
import json
import mysql.connector
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

def read_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def setup_mysql_connection():
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )

def setup_postgres_connection():
    return psycopg2.connect(os.getenv('POSTGRES_URI'))

def create_mysql_tables(conn):
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agent_insights (
            id INT AUTO_INCREMENT PRIMARY KEY,
            agent_name VARCHAR(255),
            main_point TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agent_usecases (
            id INT AUTO_INCREMENT PRIMARY KEY,
            agent_name VARCHAR(255),
            usecase_type VARCHAR(255),
            content TEXT,
            metadata JSON,
            source VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    cursor.close()

def create_postgres_tables(conn):
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agent_insights (
            id SERIAL PRIMARY KEY,
            agent_name VARCHAR(255),
            main_point TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agent_usecases (
            id SERIAL PRIMARY KEY,
            agent_name VARCHAR(255),
            usecase_type VARCHAR(255),
            content TEXT,
            metadata JSONB,
            source VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    cursor.close()

def insert_data(mysql_conn, postgres_conn, data):
    # MySQL insertion
    mysql_cursor = mysql_conn.cursor()
    
    # Insert agent insights
    for agent_name, insights in data['agent_extractions'].items():
        for insight in insights:
            mysql_cursor.execute(
                'INSERT INTO agent_insights (agent_name, main_point) VALUES (%s, %s)',
                (agent_name, insight['main_point'])
            )
    
    # Insert usecase data
    metadata = json.dumps({
        "property_type": "apartment",
        "target_audience": "medical students",
        "location_features": ["near Medicine School"],
        "amenities": ["washing machine/dryer", "fully furnished"]
    })
    
    mysql_cursor.execute(
        'INSERT INTO agent_usecases (agent_name, usecase_type, content, metadata, source) VALUES (%s, %s, %s, %s, %s)',
        ('Lisa', 'rental_ad', data['world_extraction']['Focus group']['ad_copy'], metadata, 'Focus group')
    )
    
    mysql_conn.commit()
    mysql_cursor.close()
    
    # PostgreSQL insertion
    postgres_cursor = postgres_conn.cursor()
    
    # Insert agent insights
    for agent_name, insights in data['agent_extractions'].items():
        for insight in insights:
            postgres_cursor.execute(
                'INSERT INTO agent_insights (agent_name, main_point) VALUES (%s, %s)',
                (agent_name, insight['main_point'])
            )
    
    # Insert usecase data
    postgres_cursor.execute(
        'INSERT INTO agent_usecases (agent_name, usecase_type, content, metadata, source) VALUES (%s, %s, %s, %s, %s)',
        ('Lisa', 'rental_ad', data['world_extraction']['Focus group']['ad_copy'], metadata, 'Focus group')
    )
    
    postgres_conn.commit()
    postgres_cursor.close()

def main():
    # Read JSON data
    json_file_path = 'data/extractions/appartment_rent_ad_1.extraction.json'
    data = read_json_data(json_file_path)
    
    try:
        # Setup MySQL connection and tables
        mysql_conn = setup_mysql_connection()
        create_mysql_tables(mysql_conn)
        
        # Setup PostgreSQL connection and tables
        postgres_conn = setup_postgres_connection()
        create_postgres_tables(postgres_conn)
        
        # Insert data into both databases
        insert_data(mysql_conn, postgres_conn, data)
        
        print("Data successfully inserted into both MySQL and PostgreSQL databases!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
    finally:
        # Close connections
        if 'mysql_conn' in locals():
            mysql_conn.close()
        if 'postgres_conn' in locals():
            postgres_conn.close()

if __name__ == "__main__":
    main()
