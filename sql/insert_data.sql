-- Insert data into the Organizations table
INSERT INTO my_schema.organizations (initiative, contact, name, link, scan) VALUES
('CSDI', 'Carter Shanklin', 'cartershanklin', 'https://github.com/cartershanklin', TRUE),
('CSDU', 'Parsely', 'parsely', 'https://github.com/Parsely', TRUE);

-- Insert data into the Meetings table
INSERT INTO my_schema.meetings (organization_id, date, description) VALUES
(1, '2023-01-15', 'Initial meeting with Organization Carter Shanklin'),
(2, '2023-02-20', 'Initial meeting with Organization Parsely');

-- Insert data into the Repositories table
INSERT INTO my_schema.repositories (organization_id, name, link, scan, last_scan_date) VALUES
(1, 'pyspark-cheatsheet', 'https://github.com/cartershanklin/pyspark-cheatsheet.git', TRUE, '2023-03-01'),
(2, 'pyspark-cassandra', 'https://github.com/Parsely/pyspark-cassandra.git', TRUE, '2023-03-05');
