import yaml
import os
import argparse
import logging
from git import Repo, Git

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

def main():
    """
    Main function to read repository URLs from a configuration file and clone them.
    """
    logging.basicConfig(level=logging.INFO)
    
    parser = argparse.ArgumentParser(description='Clone repositories from a configuration file.')
    parser.add_argument('--config_path', type=str, required=True, help='Path to the configuration file with repository URLs.')
    parser.add_argument('--clone_path', type=str, required=True, help='Path where repositories will be cloned.')
    args = parser.parse_args()

    with open(args.config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    repo_urls = config.get('repositories', [])
    if not repo_urls:
        logging.error("No repositories found in the configuration file.")
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
