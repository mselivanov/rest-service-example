psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
	create database $SERVICE_DB;
	create user $SERVICE_USER password '$SERVICE_PASSWORD';
	grant all privileges on database $SERVICE_DB to customer_service;
	\connect $SERVICE_DB;
	create schema customer;
	grant all privileges on schema customer to $SERVICE_USER;
EOSQL
