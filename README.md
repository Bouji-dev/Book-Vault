# BookVault 🐘📚

**Professional Library Management System with PostgreSQL**

A hands-on, project-based journey to deeply understand and master PostgreSQL using raw SQL and best practices.

### Tech Stack
- Python 3
- PostgreSQL 17+
- psycopg2 (focus on raw SQL)

## Day 1: Setup & First Connection
Features

* PostgreSQL installation verification
* Database creation (`bookvault_dev`)
* Secure connection from Python using psycopg2
* Basic version & current database queries
* Simple test table creation & data insertion

Progress
- Installed PostgreSQL (or confirmed running instance)
- Created development database `bookvault_dev`
- Established first successful connection from Python
- Executed basic diagnostic queries (`SELECT version()`, `SELECT current_database()`)
- Created and populated a test table (`test_table`)

Key Notes
- Always prefer explicit user `-U postgres` when creating databases on Windows/localhost
- Use `trust` temporarily in pg_hba.conf only for local development when password is forgotten
- Close cursor & connection properly using `finally` block
- `psycopg2.Error` is the preferred way to catch database-specific exceptions

## Day 2: Schema Design & Constraints
Features

* Understanding PostgreSQL data types (`text`, `varchar`, `timestamptz`, `bigserial`, ...)
* Proper use of constraints (`NOT NULL`, `PRIMARY KEY`, `UNIQUE`, `FOREIGN KEY`, `CHECK`)
* Initial schema: `authors` and `books` tables
* Composite UNIQUE constraint on author name
* Foreign key with `ON DELETE RESTRICT`
* Safe insertion with `ON CONFLICT DO NOTHING`

Progress
- Designed and created `authors` table with composite unique constraint
- Designed and created `books` table with CHECK constraint on publication year
- Established foreign key relationship between books and authors
- Inserted sample data (George Orwell + 1984 & Animal Farm)
- Handled possible duplicate inserts using `ON CONFLICT`

Key Notes
- Prefer `text` over `varchar(n)` unless there is a strong business length restriction
- Use `timestamptz` (not `timestamp`) for almost all date+time columns
- Foreign keys do **NOT** get automatic indexes → consider adding them manually later
- `bigserial` is safer than `serial` for future scalability
- `CHECK` constraints are excellent for catching invalid data early


### Day 3: Basic CRUD Operations + Safe Query Writing

Features

* Safe parameterized queries (protection against SQL injection)
* INSERT ... RETURNING pattern
* SELECT with JOIN + column alias
* UPDATE with condition
* DELETE with RETURNING
* Transaction management (commit / rollback)
* Helper functions for each CRUD operation

Progress
- Created reusable CRUD functions for authors and books
- Implemented safe parameterized queries everywhere
- Used RETURNING clause to get inserted/updated/deleted IDs
- Added JOIN to show author name with books
- Handled errors with try/except + rollback

Key Notes
- NEVER concatenate strings into SQL queries → always use parameters (%s, (value,))
- Use RETURNING to get generated IDs immediately after INSERT
- Manage transactions explicitly: commit on success, rollback on error
- Dictionary result from SELECT is more readable than tuples
- created_at can be updated automatically with trigger (we'll do it later)