import json
import psycopg2
import argparse
import logging
from datetime import datetime

def create_table(cursor, schema, table_name):
    """
    Create the tables in the PostgreSQL database.
    
    :param cursor: Database cursor.
    :param schema: Schema where the tables are located.
    :param table_name: Name of the main table to create.
    """
    logging.info(f"Creating tables in schema {schema}")
    cursor.execute(f"""
        CREATE SCHEMA IF NOT EXISTS {schema};

        CREATE TABLE IF NOT EXISTS {schema}.{table_name} (
            id SERIAL PRIMARY KEY,
            repository_name VARCHAR(255) NOT NULL,
            execution_date TIMESTAMP NOT NULL
        );

        CREATE TABLE IF NOT EXISTS {schema}.yaml_files (
            id SERIAL PRIMARY KEY,
            repository_id INT REFERENCES {schema}.{table_name}(id),
            yaml_file_name VARCHAR(255),
            yaml_content JSONB
        );

        CREATE TABLE IF NOT EXISTS {schema}.dependencies (
            id SERIAL PRIMARY KEY,
            repository_id INT REFERENCES {schema}.{table_name}(id),
            group_id VARCHAR(255),
            artifact_id VARCHAR(255),
            version VARCHAR(255)
        );

        CREATE TABLE IF NOT EXISTS {schema}.requirements (
            id SERIAL PRIMARY KEY,
            repository_id INT REFERENCES {schema}.{table_name}(id),
            requirement VARCHAR(255)
        );
    """)

def export_to_db(json_path, db_config, schema, table_name):
    """
    Export JSON data to the PostgreSQL database.
    
    :param json_path: Path to the JSON file.
    :param db_config: Dictionary containing database configuration.
    :param schema: Schema where the tables are located.
    :param table_name: Name of the main table to create and insert data into.
    """
    try:
        logging.info(f"Reading JSON file: {json_path}")
        with open(json_path, 'r') as file:
            data = json.load(file)
    except Exception as e:
        logging.error(f"Error reading JSON file: {e}")
        return
    
    try:
        logging.info("Connecting to the database")
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
    except Exception as e:
        logging.error(f"Error connecting to the database: {e}")
        return
    
    try:
        create_table(cursor, schema, table_name)
    except Exception as e:
        logging.error(f"Error creating table: {e}")
        return
    
    execution_date = datetime.now()
    
    try:
        for repo, repo_data in data.items():
            logging.info(f"Inserting data for repository: {repo}")
            yaml_configs = repo_data.get('yaml_configs', {})
            dependencies = repo_data.get('dependencies', [])
            requirements = repo_data.get('requirements', [])
            
            cursor.execute(f"""
                INSERT INTO {schema}.{table_name} (repository_name, execution_date)
                VALUES (%s, %s) RETURNING id
            """, (repo, execution_date))
            repo_id = cursor.fetchone()[0]
            
            for yaml_file, yaml_content in yaml_configs.items():
                cursor.execute(f"""
                    INSERT INTO {schema}.yaml_files (repository_id, yaml_file_name, yaml_content)
                    VALUES (%s, %s, %s)
                """, (repo_id, yaml_file, json.dumps(yaml_content)))
            
            for dep in dependencies:
                cursor.execute(f"""
                    INSERT INTO {schema}.dependencies (repository_id, group_id, artifact_id, version)
                    VALUES (%s, %s, %s, %s)
                """, (repo_id, dep['groupId'], dep['artifactId'], dep['version']))
            
            for req in requirements:
                cursor.execute(f"""
                    INSERT INTO {schema}.requirements (repository_id, requirement)
                    VALUES (%s, %s)
                """, (repo_id, req))
        conn.commit()
    except Exception as e:
        logging.error(f"Error inserting data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def main():
    """
    Main function to export JSON data to the PostgreSQL database.
    """
    logging.basicConfig(level=logging.INFO)
    
    parser = argparse.ArgumentParser(description='Export JSON data to the PostgreSQL database.')
    parser.add_argument('--json_path', type=str, required=True, help='Path to the JSON file.')
    parser.add_argument('--db_host', type=str, required=True, help='Database host.')
    parser.add_argument('--db_port', type=int, required=True, help='Database port.')
    parser.add_argument('--db_name', type=str, required=True, help='Database name.')
    parser.add_argument('--db_user', type=str, required=True, help='Database user.')
    parser.add_argument('--db_password', type=str, required=True, help='Database password.')
    parser.add_argument('--schema', type=str, required=True, help='Schema where the table is located.')
    parser.add_argument('--table_name', type=str, required=True, help='Name of the table to create and insert data into.')
    args = parser.parse_args()

    db_config = {
        'host': args.db_host,
        'port': args.db_port,
        'dbname': args.db_name,
        'user': args.db_user,
        'password': args.db_password
    }

    export_to_db(args.json_path, db_config, args.schema, args.table_name)

if __name__ == "__main__":
    main()
