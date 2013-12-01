-- name of the main CKAN database
\set maindb "ckan"
-- the name of the datastore database
\set datastoredb "ckan_datastore"
-- username of the ckan postgres user
\set ckanuser "ckan"
-- username of the datastore user that can write
\set wuser "ckan_datastore_readwrite"
-- username of the datastore user who has only read permissions
\set rouser "ckan_datastore_readonly"

-- revoke permissions for the read-only user
---- this step can be ommitted if the datastore not
---- on the same server as the CKAN database
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
REVOKE USAGE ON SCHEMA public FROM PUBLIC;

GRANT CREATE ON SCHEMA public TO :ckanuser;
GRANT USAGE ON SCHEMA public TO :ckanuser;

GRANT CREATE ON SCHEMA public TO :wuser;
GRANT USAGE ON SCHEMA public TO :wuser;

-- take connect permissions from main CKAN db
---- again, this can be ommited if the read-only user can never have
---- access to the main CKAN database
REVOKE CONNECT ON DATABASE :maindb FROM :rouser;

-- grant select permissions for read-only user
GRANT CONNECT ON DATABASE :datastoredb TO :rouser;
GRANT USAGE ON SCHEMA public TO :rouser;

-- grant access to current tables and views to read-only user
GRANT SELECT ON ALL TABLES IN SCHEMA public TO :rouser;

-- grant access to new tables and views by default
---- the permissions will be set when the write user creates a table
ALTER DEFAULT PRIVILEGES FOR USER :wuser IN SCHEMA public
   GRANT SELECT ON TABLES TO :rouser;
