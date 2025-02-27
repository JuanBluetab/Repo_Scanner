import json
import psycopg2
import argparse
import logging


def export_to_db(json_path, db_config):
    """
    Export JSON data to the PostgreSQL database.
    
    :param json_path: Path to the JSON file.
    :param db_config: Dictionary containing database configuration.
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
        for repo, repo_data in data.items():
            logging.info(f"Inserting data for repository: {repo}")
            yaml_configs = repo_data.get('yaml_configs', {})
            dependencies = repo_data.get('dependencies', [])
            requirements = repo_data.get('requirements', [])
            
            # Fetch the repository ID from the repositories table
            cursor.execute(f"""
                SELECT id FROM my_schema.repositories WHERE name = %s
            """, (repo,))
            repo_id = cursor.fetchone()
            
            if repo_id is None:
                logging.error(f"Repository {repo} not found in my_schema.repositories")
                continue
            
            repo_id = repo_id[0]
            
            for yaml_file, yaml_content in yaml_configs.items():
                cursor.execute(f"""
                    INSERT INTO my_schema.yaml_files (repository_id, yaml_file_name, yaml_content)
                    VALUES (%s, %s, %s)
                """, (repo_id, yaml_file, json.dumps(yaml_content)))
            
            for dep in dependencies:
                cursor.execute(f"""
                    INSERT INTO my_schema.dependencies (repository_id, group_id, artifact_id, version)
                    VALUES (%s, %s, %s, %s)
                """, (repo_id, dep['groupId'], dep['artifactId'], dep['version']))
            
            for req in requirements:
                cursor.execute(f"""
                    INSERT INTO my_schema.requirements (repository_id, requirement)
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
    args = parser.parse_args()

    db_config = {
        'host': args.db_host,
        'port': args.db_port,
        'dbname': args.db_name,
        'user': args.db_user,
        'password': args.db_password
    }

    export_to_db(args.json_path, db_config)

if __name__ == "__main__":
    main()
