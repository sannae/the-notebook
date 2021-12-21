# postgresql

!!! Resources
    * [:material-youtube: Backend master class](https://youtube.com/playlist?list=PLy_6D98if3ULEtXtNSY_2qN21VCKgoQAE) with Golang, Postgres and Docker :star:

## Getting started commands

* To send a command from bash, `sudo su - postgres -c "COMMAND"` 

* To start PostgreSQL CLI **psql**, `sudo -u postgres psql`
    * To list databases, `\l`
    * To choose a database, `\c DATABASE_NAME`
    * To show all the tables in the database, `\dt`
    * To look for a specific table in the database, `\dt *PATTERN*`
    * To create a database, `CREATE DATABASE your_db_name;`

* To test a connection to a specific database, use [pg_isready](https://www.postgresql.org/docs/current/app-pg-isready.html):
```bash
pg_isready -d <db_name> -h <host_name> -p <port_number> -U <db_user> 
```
The command `echo $?` will return the exit code of `pg_isready`, i.e.
    * `0` = the server is accepting connections normally
    * `1` = the server is rejecting connections (e.g. during startup)
    * `2` = there was no response to the connection attempt
    * `3` = no attempt was made (for example due to invalid parameters).

To test a login, try `psql -d "postgresql://USER:PASSWORD@HOST:PORT/t" -c "select now()"`.

## Random notes

* A `bigserial` type of number is a "big (8byte/64bit) autoincrementing integer"

## About db schema

* In [dbdiagram](https://dbdiagram.io/) (a quick memo about the syntax in [this holistics.io blog post](https://www.holistics.io/blog/a-database-diagram-designer-built-for-developers-and-analysts/)), the following schema instructions:
```
// Accounts
Table accounts as A {
  id bigserial [pk]
  owner varchar [not null]
  balance bigint [not null]
  currency varchar [not null]
  created_at timestamptz [not null, default: `now()`]
  
  // Just list for owner
  Indexes {
    owner
  }
}

// Entries per account
Table entries {
  id bigserial [pk]
  account_id bigint [ref: > A.id]
  amount bigint [not null, note: 'it can be negative or positive']
  created_at timestamptz [not null, default: `now()`]
  
  // Just list for account
  Indexes {
    account_id
  }
}

// Transfers between accounts
Table transfers {
  id bigserial [pk]
  from_account_id bigint [ref: > A.id]
  to_account_id bigint [ref: > A.id]
  amount bigint [not null, note: 'it must be positive']
  created_at timestamptz [not null, default: `now()`]
  
  // List for sender, receiver or both
  Indexes {
    from_account_id
    to_account_id
    (from_account_id, to_account_id) // Composite index
  }
}
```
Becomes
```sql
CREATE TABLE "accounts" (
  "id" bigserial PRIMARY KEY,
  "owner" varchar NOT NULL,
  "balance" bigint NOT NULL,
  "currency" varchar NOT NULL,
  "created_at" timestamptz NOT NULL DEFAULT (now())
);
CREATE TABLE "entries" (
  "id" bigserial PRIMARY KEY,
  "account_id" bigint,
  "amount" bigint NOT NULL,
  "created_at" timestamptz NOT NULL DEFAULT (now())
);
CREATE TABLE "transfers" (
  "id" bigserial PRIMARY KEY,
  "from_account_id" bigint,
  "to_account_id" bigint,
  "amount" bigint NOT NULL,
  "created_at" timestamptz NOT NULL DEFAULT (now())
);
ALTER TABLE "entries" ADD FOREIGN KEY ("account_id") REFERENCES "accounts" ("id");
ALTER TABLE "transfers" ADD FOREIGN KEY ("from_account_id") REFERENCES "accounts" ("id");
ALTER TABLE "transfers" ADD FOREIGN KEY ("to_account_id") REFERENCES "accounts" ("id");
CREATE INDEX ON "accounts" ("owner");
CREATE INDEX ON "entries" ("account_id");
CREATE INDEX ON "transfers" ("from_account_id");
CREATE INDEX ON "transfers" ("to_account_id");
CREATE INDEX ON "transfers" ("from_account_id", "to_account_id");
COMMENT ON COLUMN "entries"."amount" IS 'it can be negative or positive';
COMMENT ON COLUMN "transfers"."amount" IS 'it must be positive';
```
Notice the `bigserial` number type and the `now()` function in the dbdiagram syntax, which are specifically selected to be exported to PostgreSQL.

## Deploy on [:material-docker: Docker](./../infrastructure/docker.md)

* All the steps to set up a running `postgres` Docker container are exhaustively explained in the [description of the official postgres image](https://hub.docker.com/_/postgres?tab=description) on Docker Hub.

* To run *.sql scripts on a postgres container, 
    1. Copy your `SCRIPT.sql` file to the `CONTAINER_NAME` running container's root:
    ```bash
    docker container cp SCRIPT.sql CONTAINER_NAME:/
    ```
    2. Verify that the file is there:
    ```bash
    docker container exec -it CONTAINER_NAME bash
    ```
    Then `ls SCRIPT*`
    3. Instruct the `psql` client to run the file you just copied as the default username `root` on the database `your_database_name`
    ```bash
    docker container exec -it CONTAINER_NAME psql --dbname=your_database_name --username root -f /SCRIPT.sql
    ```

!!! warning
    This whole sequence could probably be bypassed by using a Dockerfile

## Migrations

To easily perform migrations on PostgreSQL, you may use the [:material-github: golang-migrate](https://github.com/golang-migrate/migrate) CLI tool, written in [:language-go: Go](https://golang.org/). 

```bash
# Install golang-migrate
brew install golang-migrate

# Test installation
migrate -version

# Create the db migrations folder in your project folder
mkdir -p db/migrations

# Create your first migration
migrate create -ext sql -dir db/migrations -seq initial_schema
``` 

The last command will create the first migration called `initial_schema` in files with `.sql` extension, in the path specified by `-dir` and with a sequential (`-seq`) number to keep track of progressing migrations. The first two files are:

```bash
./db/migrations/000001_initial_schema.up.sql      # Script to "migrate up", i.e. moving forward in migrations 
./db/migrations/000001_initial_schema.down.sql    # Script to "migrate down", i.e. moving backwards in migrations
```

If you wish to do it manually, copy your schema creation script in the first file, and edit the second file with the reverse commands (i.e. dropping every object in the database).

To run your first migration, use:

```bash
migrate -path ./db/migrations -database "postgresql://USERNAME:PASSWORD@HOSTNAME:PORT/DATABASE_NAME?PARAMETERS" -verbose up
```

Where:
* the `-database` switch requires the whole [:material-github: database URL](https://github.com/golang-migrate/migrate#database-urls)
* the `up` argument specifies the direction of the migration
* the `PARAMETERS` (more specifically `?PARAMETER1=VALUE1&PARAMETER2=VALUE2`) can be used to add any additional parameter

!!! warning
    If you encounter the **SSL is not enabled on the server** error (like in a [Docker](../cloud/docker.md) PostgreSQL container), use the `?sslmode=disable` parameter after the `DATABASE_NAME` in the URL.

The first migration (containing the schema initialization scripts) will also add the `schema_migrations` table in the database.
