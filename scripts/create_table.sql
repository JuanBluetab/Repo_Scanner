CREATE SCHEMA IF NOT EXISTS my_schema;

CREATE TABLE my_schema.repository_data (
    id SERIAL PRIMARY KEY,
    repository_name VARCHAR(255) NOT NULL,
    yaml_file_name VARCHAR(255) NOT NULL,
    yaml_content JSONB NOT NULL,
    dependency_group_id VARCHAR(255),
    dependency_artifact_id VARCHAR(255),
    dependency_version VARCHAR(255),
    requirement VARCHAR(255)
);
