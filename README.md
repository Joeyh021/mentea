# Group 32 CS261 Software Engineering Project

If you can come up with a more fancy name please let us know

## Getting Started with Development

### Requirements

- Python 3.10
  - Python can be installed using your favourite package manager, or using the installers downloaded from [python.org](https://www.python.org/downloads/)
- Poetry
  - Poetry is a dependancy and environment managment tool for python. It simplifies working with virtual environments and allows to specify all the project settings and dependencies.
  - It can be installed following the instructions from <https://python-poetry.org/docs/#installation>

### Installation

- Clone the project to your local machine
- Set up the virtual environment using `poetry install`
  - This will create a new python venv that you can activate using `poetry shell`

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
- CI is currently gated on `mypy`, `black`, and `pytest` all passing. If any of these throw errors, you won't be able to merge code into the repo

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
