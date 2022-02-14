# Group 32 CS261 Software Engineering Project

If you can come up with a more fancy name please let us know

## Getting Started with Development

### Requirements

- Python 3.10
  - Python can be installed using your favourite package manager, or using the installers downloaded from [python.org](https://www.python.org/downloads/)
- Poetry
  - Poetry is a dependancy and environment managment tool for python. It simplifies working with virtual environments and allows to specify all the project settings and dependencies.
  - It can be installed following the instructions from <https://python-poetry.org/docs/#installation>
- PostgreSQL
  - Postgres will be used as the backend database for django
  - It can be installed following the instructios from <https://www.postgresql.org/download/>

### Installation

- Clone the project to your local machine
- Set up the virtual environment using `poetry install`
  - This will create a new python venv that you can activate using `poetry shell`
- Create a local PostgreSQL database using the psql command line utility (`sudo su postgres` then `psql`)
  - `CREATE USER softeng WITH password 'password';`
  - `CREATE DATABASE softeng WITH OWNER = softeng;`
  - You can use different user names/passwords/database names but you will need to edit the connection settings in `dev.py` if you do so. DO NOT COMMIT THESE CHANGES.
- Run `poetry run manage migrate` to create the database tables
- Run `poetry run python manage.py runserver` to start the development server. You can now access the site at `localhost:8000` in your web browser.

### Usage

- `poetry run` can be used to run python and other scripts/tools within the venv
- `poetry run python` should be used instead of just `python` so code is executed within the project instead of your machine's global environment
- `poetry run <tool>` can be used to run another tool or script that has been installed into the virtual environment, such as `black` or `mypy`

### Tooling

- `mypy` is a static type checker which looks at type hints in the code and finds type erorrs before runtime
  - You should set this up within your IDE, and run it before committing changes
  - `mypy` _will_ moan at you. This is the point.
- `black` is a code formatter to ensure that all code in the repo conforms to the same style guide
  - Reviewing commits is a lot harder when 90% of the changes are whitespace and formatting
  - Set this up in your IDE too, and run it before committing changes
- `pytest` is a testing tool used to handle unit and integration tests
  - Run `pytest` to make sure any changes you made haven't broken anything
- `pylint` is a linter used to catch common issues in python code.
  - This will throw some false positives but is useful to catch common errors and point out things that are typically easily missed
- CI is currently gated on `mypy`, `black`, and `pytest` all passing. If any of these throw errors, you won't be able to merge code into the repo
  - Just because it isn't also gated on `pylint` doesn't mean you shouldn't check code with it, as it also makes life easier for the person reviewing your code

### Editing the Client side form system
- If you don't need to make any changes then please don't!
- If you are planning on making changes then:
  - Run npm install
  - If typescript doesn't work then install it with npm globally `npm install -g typescript`
  - Run the bundle script `npm run bundle` command to build the code, it will automatically watch for changes
    - You can optionally run the `type-check:watch` to provide realtime typescript errors
- If you haven't made any changes then the production script in `static/js/dist` is all you need. IT IS ALREADY INCLUDED IN `base.html`.
- If you need any help then just ask :)
## Best Practices

- Work on a new branch for each feature, bug fix, or series of commits you intend to make.
- Create a PR if you want to merge a branch into main
  - PRs need approval from at least one other person just to double check no one does anything wacky
  - Github won't let you push directly to main anyway
- Keep commits as atomic as possible, don't commit a day's worth of work in one go
- Make good use of the tooling to keep your code clean and bug free
- WRITE TESTS. I MEAN IT.
  - Write tests before or at the same time you are writing the code you intend to test
  - `pytest --cov` will give a code coverage report which tells you how much of your code is covered by the tests. Use this to help write comprehensive tests
- Document code as you write it using module, class, and function docstrings
  - `pylint` will pick up any that you miss
- Comment code thoroughly

## Useful Django tips

- When writing views, use class-based views as opposed to functions-based views. This is because class-based views have a lot of extra functionality, and allow a single view to do both GET and POST requests. See the Django documentation ([here](https://docs.djangoproject.com/en/4.0/topics/class-based-views/) and [here](https://docs.djangoproject.com/en/4.0/topics/class-based-views/mixins/)) for more details.
- UUIDs should be used as the `id` field for all models. While Django does auto-provide an ID field, we need to manually specify the field in each model and mark it as UUID. The field will look something like `id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)` (with `import uuid` at the top of the file)
