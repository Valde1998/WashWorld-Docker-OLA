-- Startup creates missing tables; normal requests only read and change rows.
REVOKE ALL PRIVILEGES ON cleanwash.* FROM 'washworld'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE ON cleanwash.* TO 'washworld'@'%';
