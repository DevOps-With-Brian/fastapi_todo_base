# Project 3
Just a test project with overall starting points with FastAPI including auth using hashed pw's, and Todo model's.

## Setting Up
Just setup a python venv:

`python -m venv .venv`

Activate It:

`source .venv/bin/activate`

Install the Requirements:

`pip install -r requirements.txt`

Copy the `env.example` to `.env` file for environment vars.  Will be changing to doppler soon.

Run the project:

`cd TodoApp && uvicorn main:app --reload`


## Database Migrations
The database migrations use Alembic.

Common commands:

`alembic init <folder name>` - Initializes a new, generic environment

`alembic revision -m <message>` - Creates a new revision of the environment

`alembic upgrade <revision #>` - Run our upgrade migration to our database

`alembic downgrade -1` - Run our downgrade migration to our databse

### Adding New Column
Before updating the code you can create a migration via the `alembic revision -m "Revision Message"` and this will create a new version file you would modify to create the column correctly like `op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))` in the upgrade for example to add a new column to the `users` table called `phone_number` that is a string.

Then this will create the object on the users that exist and allow you to then update the code and create this in the model and use it.  Ensure you also setup the drop method as well to drop the column like `op.drop_column('users', 'phone_number')`