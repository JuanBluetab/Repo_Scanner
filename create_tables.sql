-- Table Organizations
CREATE TABLE my_schema.organizations (
    id SERIAL PRIMARY KEY,
    initiative VARCHAR(255) NOT NULL,
    contact VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    link VARCHAR(255),
    scan BOOLEAN DEFAULT FALSE
);

-- Table Meetings
CREATE TABLE my_schema.meetings (
    id SERIAL PRIMARY KEY,
    organization_id INT NOT NULL,
    date DATE NOT NULL,
    description TEXT,
    FOREIGN KEY (organization_id) REFERENCES organizations(id)
);

-- Table Repositories
CREATE TABLE my_schema.repositories (
    id SERIAL PRIMARY KEY,
    organization_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    link VARCHAR(255) NOT NULL,
    scan BOOLEAN DEFAULT FALSE,
    last_scan_date DATE,
    FOREIGN KEY (organization_id) REFERENCES organizations(id)
);
