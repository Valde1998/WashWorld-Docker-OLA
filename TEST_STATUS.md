# Test status

Tested on **8 October 2026**, approximately 02:20–02:28 CEST (UTC+02:00).

Application source tested at commit `bddf6b5f4bfdc534ee27055cfaeda161a8badc03`, using Docker Desktop 4.72.0 with Linux containers via WSL2, Docker Engine 29.4.2 and Docker Compose v5.1.3.

The test used the local checkout, separate environment values and a fresh MariaDB volume under Compose project `washworld-ola-test`. Its volume was `washworld-ola-test_cleanwash_data`. Existing WashWorld data was not used or removed. The normal README startup uses the project's default name, `washworld-ola`.

## Passed checks

| Check | Observed result |
|---|---|
| Compose validation | `docker compose config --quiet` completed successfully. |
| Docker builds | Frontend and backend images built successfully. Next.js build and TypeScript checks passed. |
| Startup | `up --build -d --wait --wait-timeout 180` succeeded; frontend, backend and MariaDB became healthy. |
| Backend unit tests in Docker | All **19 tests passed**. These tests use mocks. |
| Frontend lint in Docker | `npm run lint` passed in the Dockerfile's build-stage image. |
| Real database integration | **16 checks passed before restart**, covering readiness, 71 seeded locations, membership plans, login, authenticated profile reads/writes, wash-history reads/writes, rejected invalid inputs and CORS. |
| Container removal and recreation | `down` without `-v`, followed by `up -d --wait --wait-timeout 180`, succeeded with the same database volume. |
| Integration after recreation | **14 checks passed**, including login and the preserved profile name and wash-history entry. These repeat relevant checks from the first phase; they are not 14 additional distinct features. |
| Browser with real API/database | Login opened Home; Activity showed the saved wash and 71 locations after container recreation. Profile data loaded correctly. A phone-field change saved through the browser remained after reloading. |
| Password handling | The database stored a hash that validated against the test password. The profile API did not return a password or hash. |
| Rejected requests | Missing JWT: 401; invalid JWT: 422; incorrect password: 401; invalid wash location: 400. |
| CORS | The configured frontend origin received the expected CORS header; an unrelated origin did not. |

The profile name `Docker Persistence Test` and wash type `Docker persistence check` were written through the API before `down`. Both were read back after the containers were recreated. This tests a named volume rather than only stopping and restarting the same container.

No failure was found in these checks. This does not establish that every app feature or possible input works.

## Runtime configuration verified

- Frontend: `uid=1000(node)`; backend: `uid=10001(app)`.
- Both appservices: `cap_drop: ALL`, `no-new-privileges:true`.
- Frontend and backend host ports: `127.0.0.1:3000` and `127.0.0.1:5001`.
- MariaDB: no published host port, only the internal `data` network, named volume mounted at `/var/lib/mysql`.
- Backend: both `web` and `data`; frontend: only `web`.
- Database app user: `washworld`, with SELECT, INSERT, UPDATE, DELETE and CREATE on `cleanwash.*`, not DB-root.
- Docker engine security options included seccomp and cgroupns; **rootless mode was not configured**. Non-root app users and a rootless engine are different properties.

## Measured resource use

Measured at **02:28:07 CEST on 8 October 2026**, using `docker compose stats --no-stream` after ordinary browser/API use. Periodic health checks were still active. There was no systematic load test. CPU values are snapshots, not averages or evidence of maximum capacity.

| Service | RAM use | RAM limit | CPU snapshot | CPU limit |
|---|---:|---:|---:|---:|
| Frontend | 42.29 MiB | 512 MiB | 26.57% | 1 CPU |
| Backend | 42.86 MiB | 512 MiB | 0.03% | 1 CPU |
| MariaDB | 65.02 MiB | 768 MiB | 0.01% | 1 CPU |

`docker inspect` confirmed the configured memory and CPU limits. Limits constrain the services; they do not reserve that amount of memory or describe actual usage.

Image sizes reported by `docker image inspect --format '{{.Size}}'`:

| Image | Bytes | Approximate MiB |
|---|---:|---:|
| Frontend runtime | 85,379,342 | 81.4 |
| Frontend build stage | 276,013,754 | 263.2 |
| Backend runtime | 65,566,760 | 62.5 |
| MariaDB | 121,041,900 | 115.4 |

The frontend runtime image was about 69% smaller than its build-stage image in this measurement. This is evidence of the staged-build benefit, not a measurement of all Docker cache or Windows disk usage.

## Recorded evidence and repeating the checks

The records contain test results and selected runtime fields, without environment secrets, passwords or JWTs:

- [API results before/after recreation](docs/test-evidence/2026-10-08/api-results.json).
- [Backend unit-test output](docs/test-evidence/2026-10-08/backend-unit-tests.txt).
- [Selected runtime configuration](docs/test-evidence/2026-10-08/runtime-evidence.json).
- [Timestamped resource measurement](docs/test-evidence/2026-10-08/resource-measurements.json).

Follow the [README](README.md) to start the stack, create your own demo user, run the unit tests and repeat the profile persistence test. Record new resource measurements on your own machine. The 30 integration-check records came from a separate test harness; they are historical evidence, not an additional test suite installed by the normal startup commands.

## Not tested and known limitations

- Actual SMTP/Brevo email delivery and the full email-verification/password-reset flows. Email is not configured by default; the tested login used the local demo-user helper.
- The existing Cypress suite. It mocks API responses and would not by itself prove the MariaDB connection.
- Optional phpMyAdmin, cloud deployment and performance under systematic load.
- All remaining app and security scenarios, including cross-user isolation; the listed JWT/input checks are not a complete security audit.
- Payment or QR display as real commercial services.

There is no source-code bind mount for hot reload; persistence was tested through the database volume. The Docker engine is not rootless. Presentation booking, the group presentation and repository-link submission are outside these technical test results.
