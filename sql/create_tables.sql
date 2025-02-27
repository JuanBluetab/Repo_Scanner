-- Schema: my_schema
CREATE SCHEMA IF NOT EXISTS my_schema;

-- Table Organizations
CREATE TABLE IF NOT EXISTS my_schema.organizations (
    id SERIAL PRIMARY KEY,
    initiative VARCHAR(255) NOT NULL,
    contact VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    link VARCHAR(255),
    scan BOOLEAN DEFAULT FALSE
);

-- Table Meetings
CREATE TABLE IF NOT EXISTS my_schema.meetings (
    id SERIAL PRIMARY KEY,
    organization_id INT NOT NULL,
    date DATE NOT NULL,
    description TEXT,
    FOREIGN KEY (organization_id) REFERENCES organizations(id)
);

-- Table Repositories
CREATE TABLE IF NOT EXISTS my_schema.repositories (
    id SERIAL PRIMARY KEY,
    organization_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    link VARCHAR(255) NOT NULL,
    scan BOOLEAN DEFAULT FALSE,
    last_scan_date DATE,
    FOREIGN KEY (organization_id) REFERENCES organizations(id)
);

-- Table Requirements
CREATE TABLE IF NOT EXISTS my_schema.requirements (
    id SERIAL PRIMARY KEY,
    repository_id INT NOT NULL,
    requirement VARCHAR(255),
    FOREIGN KEY (repository_id) REFERENCES repositories(id)
);

-- Table YAML Files
CREATE TABLE IF NOT EXISTS my_schema.yaml_files (
    id SERIAL PRIMARY KEY,
    repository_id INT NOT NULL,
    yaml_file_name VARCHAR(255),
    yaml_content JSONB,
    FOREIGN KEY (repository_id) REFERENCES repositories(id)
);

-- Table Dependencies
CREATE TABLE IF NOT EXISTS my_schema.dependencies (
    id SERIAL PRIMARY KEY,
    repository_id INT NOT NULL,
    group_id VARCHAR(255),
    artifact_id VARCHAR(255),
    version VARCHAR(255),
    FOREIGN KEY (repository_id) REFERENCES repositories(id)
);
