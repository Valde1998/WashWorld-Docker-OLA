# Test status

Tested on 8 October 2026 using Docker Desktop with Linux containers and Compose project `washworld-ola`.

## Results

- `docker compose up --build -d` built the app, and all three services became healthy. The test run used `--wait` to wait for health checks.
- All 19 backend unit tests passed. These use mocks.
- 20 integration checks passed before removing the containers, and 16 passed after recreating them. These used the real MariaDB database.
- The checks covered login, profile changes, wash history, input validation, CORS and separation of users' wash histories.
- A profile change and saved wash survived `docker compose down` followed by `docker compose up`, without `-v`.
- The frontend at localhost:3000 and backend readiness at localhost:5001/health/ready returned HTTP 200 from Windows.
- Frontend runs as UID 1000 and backend as UID 10001. Both are non-root.

The integration checks used a temporary test tool outside this repository. It is not needed to run the project. The generated test accounts were removed afterward.

## Resource use

Measured with Compose stats at 14:57:25 CEST after the integration checks, with health checks active:

| Service | Memory / limit | CPU |
|---|---|---|
| frontend | 32.53MiB / 512MiB | 8.75% |
| backend | 42.3MiB / 512MiB | 53.54% |
| mariadb | 60.28MiB / 768MiB | 0.14% |

These are snapshots, not a load test. Compose limits frontend/backend to 512 MiB each and MariaDB to 768 MiB, with one CPU per service.

## Limitations

Email flows, Cypress, phpMyAdmin and systematic load testing have not been tested. The checks do not cover every application or security scenario.

The Docker Desktop engine is not rootless. Non-root app users are a separate protection. The [original OLA](https://ek.itslearning.com/main.aspx?CourseID=7577&ElementID=1566430&ElementType=131072) mentions rootless, so this setup records it as a limitation rather than claiming to meet that point.

Follow the [README](README.md) to repeat the unit tests and profile persistence check. Booking, repository submission and the group presentation are outside these technical checks.
