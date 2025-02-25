import os
import json
import shutil
import logging
import argparse
import xml.etree.ElementTree as ET

def update_requirements(requirements, new_version="3.5.0"):
    """
    Update the Spark version in the requirements list.
    
    :param requirements: List of requirements as strings.
    :param new_version: The new version to update to.
    :return: Updated list of requirements.
    """
    logging.info("Updating Spark version in requirements.txt")
    updated_requirements = []
    try:
        for req in requirements:
            if req.startswith("pyspark=="):
                logging.info(f"Updating {req} to pyspark=={new_version}")
                updated_requirements.append(f"pyspark=={new_version}")
            else:
                updated_requirements.append(req)
    except Exception as e:
        logging.error(f"Error updating requirements: {e}")
    return updated_requirements

def update_pom_file(xml_path):
    """
    Update the pom.xml file with the new dependencies.
    
    :param xml_path: Path to the pom.xml file.
    """
    logging.info(f"Updating pom.xml file at {xml_path}")
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        namespaces = {'mvn': 'http://maven.apache.org/POM/4.0.0'}
        
        for dependency in root.findall('.//mvn:dependency', namespaces):
            group_id = dependency.find('mvn:groupId', namespaces).text
            artifact_id = dependency.find('mvn:artifactId', namespaces).text
            if group_id == 'org.apache.spark':
                version_element = dependency.find('mvn:version', namespaces)
                logging.info(f"Updating {artifact_id} from version {version_element.text} to 3.5.0")
                version_element.text = '3.5.0'
        
        tree.write(xml_path)
    except Exception as e:
        logging.error(f"Error updating pom.xml: {e}")

def copy_and_update_repos(base_path, new_base_path, scan_results_path):
    """
    Copy repositories to a new location and update Spark dependencies to version 3.5 if necessary.
    
    :param base_path: Original base path to the repositories.
    :param new_base_path: New base path for the copied repositories.
    :param scan_results_path: Path to the scan results JSON file.
    """
    logging.info(f"Copying repositories from {base_path} to {new_base_path}")
    try:
        if not os.path.exists(new_base_path):
            os.makedirs(new_base_path)
        
        with open(scan_results_path, 'r') as file:
            scan_results = json.load(file)
        
        for repo, repo_data in scan_results.items():
            original_repo_path = os.path.join(base_path, repo)
            new_repo_path = os.path.join(new_base_path, repo)
            shutil.copytree(original_repo_path, new_repo_path)
            logging.info(f"Copied repository {repo} to {new_repo_path}")

            # Update dependencies in the copied repository
            if 'dependencies' in repo_data:
                xml_path = os.path.join(new_repo_path, 'pom.xml')
                if os.path.exists(xml_path):
                    logging.info(f"Updating pom.xml at {xml_path}")
                    update_pom_file(xml_path)
            
            # Update requirements.txt in the copied repository
            if 'requirements' in repo_data:
                updated_requirements = update_requirements(repo_data['requirements'])
                req_path = os.path.join(new_repo_path, 'requirements.txt')
                if os.path.exists(req_path):
                    logging.info(f"Updating requirements.txt at {req_path}")
                    with open(req_path, 'w') as req_file:
                        req_file.write("\n".join(updated_requirements))
    except Exception as e:
        logging.error(f"Error copying and updating repositories: {e}")

def main():
    """
    Main function to copy repositories and update Spark dependencies to version 3.5.
    """
    logging.basicConfig(level=logging.INFO)
    
    parser = argparse.ArgumentParser(description='Copy repositories and update Spark dependencies to version 3.5.')
    parser.add_argument('--base_path', type=str, required=True, help='Base path to the repositories.')
    parser.add_argument('--new_base_path', type=str, required=True, help='New base path for the copied repositories.')
    parser.add_argument('--scan_results_path', type=str, required=True, help='Path to the scan results JSON file.')
    args = parser.parse_args()

    try:
        copy_and_update_repos(args.base_path, args.new_base_path, args.scan_results_path)
    except Exception as e:
        logging.error(f"Error in main function: {e}")

if __name__ == "__main__":
    main()
