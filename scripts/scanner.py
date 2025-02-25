import yaml
import xml.etree.ElementTree as ET
import os
import json
import argparse
import logging

def scan_yaml(yaml_path):
    """
    Scan a YAML file and return its contents as a dictionary.
    
    :param yaml_path: Path to the YAML file.
    :return: Dictionary containing the YAML file contents.
    """
    logging.info(f"Scanning YAML file: {yaml_path}")
    with open(yaml_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def scan_pom(xml_path):
    """
    Scan a Maven POM file and return a list of dependencies.
    
    :param xml_path: Path to the POM file.
    :return: List of dictionaries containing dependency information.
    """
    logging.info(f"Scanning POM file: {xml_path}")
    tree = ET.parse(xml_path)
    root = tree.getroot()
    namespaces = {'mvn': 'http://maven.apache.org/POM/4.0.0'}
    dependencies = []
    for dependency in root.findall('.//mvn:dependency', namespaces):
        try:
            group_id = dependency.find('mvn:groupId', namespaces).text
            artifact_id = dependency.find('mvn:artifactId', namespaces).text
            version = dependency.find('mvn:version', namespaces).text
            dependencies.append({
                'groupId': group_id,
                'artifactId': artifact_id,
                'version': version
            })
        except AttributeError:
            continue  # Skip dependencies with missing information
    return dependencies

def scan_requirements(req_path):
    """
    Scan a requirements.txt file and return a list of requirements.
    
    :param req_path: Path to the requirements.txt file.
    :return: List of requirements as strings.
    """
    logging.info(f"Scanning requirements file: {req_path}")
    with open(req_path, 'r') as file:
        requirements = file.readlines()
    return [req.strip() for req in requirements]

def write_to_json(data, output_path):
    """
    Write data to a JSON file.
    
    :param data: Data to write to the JSON file.
    :param output_path: Path to the output JSON file.
    """
    logging.info(f"Writing data to JSON file: {output_path}")
    with open(output_path, 'w') as file:
        json.dump(data, file, indent=4)

def write_to_txt(data, output_path):
    """
    Write data to a text file in a human-readable format.
    
    :param data: Data to write to the text file.
    :param output_path: Path to the output text file.
    """
    logging.info(f"Writing data to text file: {output_path}")
    with open(output_path, 'w') as file:
        for repo, repo_data in data.items():
            file.write(f"Repository: {repo}\n")
            file.write("YAML Configs:\n")
            for yaml_file, yaml_config in repo_data['yaml_configs'].items():
                file.write(f"  {yaml_file}:\n")
                for key, value in yaml_config.items():
                    file.write(f"    {key}: {value}\n")
            file.write("Dependencies:\n")
            for dep in repo_data['dependencies']:
                file.write(f"  - groupId: {dep['groupId']}, artifactId: {dep['artifactId']}, version: {dep['version']}\n")
            if 'requirements' in repo_data:
                file.write("Requirements:\n")
                for req in repo_data['requirements']:
                    file.write(f"  - {req}\n")
            file.write("\n")

def main():
    """
    Main function to scan repositories for configuration files and dependencies,
    and write the results to JSON and text files.
    """
    logging.basicConfig(level=logging.INFO)
    
    parser = argparse.ArgumentParser(description='Scan repositories for configuration files and dependencies.')
    parser.add_argument('--base_path', type=str, required=True, help='Base path to the repositories.')
    parser.add_argument('--json_output_path', type=str, required=True, help='Path to the output JSON file.')
    parser.add_argument('--txt_output_path', type=str, required=True, help='Path to the output text file.')
    args = parser.parse_args()

    data = {}

    for repo in os.listdir(args.base_path):
        repo_path = os.path.join(args.base_path, repo)
        logging.info(f"Scanning repository: {repo}")
        yaml_configs = {}
        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith('.yaml'):
                    yaml_path = os.path.join(root, file)
                    yaml_configs[file] = scan_yaml(yaml_path)
        
        xml_path = os.path.join(repo_path, 'pom.xml')
        req_path = os.path.join(repo_path, 'requirements.txt')

        repo_data = {
            'yaml_configs': yaml_configs,
            'dependencies': scan_pom(xml_path) if os.path.exists(xml_path) else []
        }

        if os.path.exists(req_path):
            repo_data['requirements'] = scan_requirements(req_path)

        if yaml_configs or repo_data['dependencies'] or 'requirements' in repo_data:
            data[repo] = repo_data

    write_to_json(data, args.json_output_path)
    write_to_txt(data, args.txt_output_path)

if __name__ == "__main__":
    main()
