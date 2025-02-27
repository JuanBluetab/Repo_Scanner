import psycopg2
import argparse
import logging

def execute_sql_file(cursor, file_path):
    """
    Execute SQL commands from a file.
    
    :param cursor: Database cursor.
    :param file_path: Path to the SQL file.
    """
    logging.info(f"Executing SQL file: {file_path}")
    with open(file_path, 'r') as file:
        sql = file.read()
        cursor.execute(sql)

def clear_tables(cursor):
    """
    Clear all data from the existing tables.
    
    :param cursor: Database cursor.
    """
    logging.info("Clearing existing tables")
    tables = ['dependencies', 'yaml_files', 'requirements', 'repositories', 'meetings', 'organizations']
    for table in tables:
        cursor.execute(f"TRUNCATE TABLE my_schema.{table} CASCADE;")

def initialize_db(db_config):
    """
    Initialize the database by creating tables and inserting base data.
    
    :param db_config: Dictionary containing database configuration.
    """
    try:
        logging.info("Connecting to the database")
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
    except Exception as e:
        logging.error(f"Error connecting to the database: {e}")
        return
    
    try:
        # Set the search path to the schema
        cursor.execute(f"SET search_path TO my_schema;")
        clear_tables(cursor)
        execute_sql_file(cursor, f'../sql/create_tables.sql')
        conn.commit()
    except Exception as e:
        logging.error(f"Error executing SQL file: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def main():
    """
    Main function to initialize the database.
    """
    logging.basicConfig(level=logging.INFO)
    
    parser = argparse.ArgumentParser(description='Initialize the PostgreSQL database.')
    parser.add_argument('--db_host', type=str, required=True, help='Database host.')
    parser.add_argument('--db_port', type=int, required=True, help='Database port.')
    parser.add_argument('--db_name', type=str, required=True, help='Database name.')
    parser.add_argument('--db_user', type=str, required=True, help='Database user.')
    parser.add_argument('--db_password', type=str, required=True, help='Database password.')
    args = parser.parse_args()

    db_config = {
        'host': args.db_host,
        'port': args.db_port,
        'dbname': args.db_name,
        'user': args.db_user,
        'password': args.db_password
    }

    initialize_db(db_config)

if __name__ == "__main__":
    main()
