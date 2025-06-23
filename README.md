# Domestic E-commerce Anti-counterfeiting Code System

This repository contains the codebase for generating and verifying anti-counterfeiting codes for domestic e-commerce products.

## Documentation

- [Project overview](docs/SPU_static_anti_counterfeiting_project.md)
- [Database ERD](docs/ERD.md)
- [OpenAPI specification](docs/openapi.yaml)
- SQL schema is located in [sql/spu_channel_code.sql](sql/spu_channel_code.sql)

## Code

The Python modules live under `src/anticounterfeiting` and include:

- `generator.py` – generate codes for each SPU and channel and store them in the database.
- `tasks.py` – Celery task for rendering QR codes to a NAS path.

Run tests with `pytest` and lint with `ruff`.
