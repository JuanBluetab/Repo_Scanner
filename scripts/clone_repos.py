import os
import argparse
import logging
from git import Repo, Git
import psycopg2

# Configurar GitPython para usar el ejecutable de Git explícitamente
git_executable_path = r"C:\Users\juan.jimenez_bluetab\AppData\Local\Atlassian\SourceTree\git_local\cmd\git.exe"
Git.refresh(git_executable_path)

def clone_repo(repo_url, clone_path):
    """
    Clone a repository from a given URL to a specified path.
    
    :param repo_url: URL of the repository to clone.
    :param clone_path: Path where the repository will be cloned.
    """
    logging.info(f"Cloning repository: {repo_url} into {clone_path}")
    Repo.clone_from(repo_url, clone_path)

def get_repositories_to_clone(db_config, schema):
    """
    Get the list of repositories to clone from the database.
    
    :param db_config: Database configuration dictionary.
    :param schema: Schema name in the database.
    :return: List of repository URLs to clone.
    """
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    query = f"""
    SELECT r.link
    FROM {schema}.organizations o
    JOIN {schema}.repositories r ON o.id = r.organization_id
    WHERE o.scan = TRUE AND r.scan = TRUE;
    """
    cursor.execute(query)
    repo_urls = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return repo_urls

def main():
    """
    Main function to read repository URLs from the database and clone them.
    """
    logging.basicConfig(level=logging.INFO)
    
    parser = argparse.ArgumentParser(description='Clone repositories from the database.')
    parser.add_argument('--db_host', type=str, required=True, help='Database host.')
    parser.add_argument('--db_port', type=str, required=True, help='Database port.')
    parser.add_argument('--db_name', type=str, required=True, help='Database name.')
    parser.add_argument('--db_user', type=str, required=True, help='Database user.')
    parser.add_argument('--db_password', type=str, required=True, help='Database password.')
    parser.add_argument('--schema', type=str, required=True, help='Schema name in the database.')
    parser.add_argument('--clone_path', type=str, required=True, help='Path where repositories will be cloned.')
    args = parser.parse_args()

    db_config = {
        'host': args.db_host,
        'port': args.db_port,
        'dbname': args.db_name,
        'user': args.db_user,
        'password': args.db_password
    }

    repo_urls = get_repositories_to_clone(db_config, args.schema)
    if not repo_urls:
        logging.error("No repositories found to clone.")
        return
    
    for repo_url in repo_urls:
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        repo_clone_path = os.path.join(args.clone_path, repo_name)
        if not os.path.exists(repo_clone_path):
            clone_repo(repo_url, repo_clone_path)
        else:
            logging.info(f"Repository {repo_name} already exists at {repo_clone_path}")

if __name__ == "__main__":
    main()
