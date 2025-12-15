# polimatch

Simple face verification helper used to search and verify member photos.

## Quick start

- Install dependencies (in a virtualenv):

```bash
pip install -r requirements.txt
```

- Run the batch verifier (example):

```bash
# from project root
python -m src.verification.batch_processor
```

## Configuration

- Place project-level configuration in `config.json` (see example in repository).

## Testing & Coverage

- Run tests with `pytest`:

```bash
pytest
```

- Run tests with coverage:

```bash
pytest --cov=src --cov-report=term-missing
```

## Notes

- Keep `config.json` out of version control if it contains secrets; use environment variables instead.
- The repository uses a `src/` layout; when running tests or modules directly make sure to run from the project root so imports resolve correctly.

## Contact

Author: Jeesang Kim <jeenowden@gmail.com>
