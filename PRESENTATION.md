# Presentation notes

## 0–1 minutes: the project

WashWorld is an existing car wash app with a Next.js frontend, Flask backend and MariaDB database. Docker Compose runs them together so developers do not need to install each part separately.

## 1–3 minutes: architecture

- An image contains the app and its runtime; a container runs that image.
- The browser reaches frontend port 3000 and backend port 5001 on localhost.
- The frontend and backend share `web`. The backend finds `mariadb:3306` on the internal `data` network; MariaDB has no host port.
- The `cleanwash_data` named volume stores the database at `/var/lib/mysql` and survives container removal.
- Readiness checks make MariaDB ready before the backend starts, then the backend ready before the frontend starts.

Show the actual service, network and volume names in `docker-compose.yml`. Explain that Compose prefixes network and volume names with its project name.

## 3–5 minutes: implementation choices

Open the Dockerfiles and relevant Compose sections. Explain two or three choices:

- The frontend's dependencies/build/runtime stages keep development packages out of the final image. The backend also separates dependency installation from its runtime.
- Frontend and backend app processes run as non-root users (`node` and `app`), drop capabilities and prevent privilege escalation. **The tested Docker engine is not rootless.** Do not describe a `USER` instruction as proof of a rootless engine.
- Secrets come from a local `.env`, which is not shared on GitHub. Do not display its contents.
- CPU/RAM limits constrain resource use; they are different from the actual usage shown by `stats`.

## 5–8 minutes: live demo

Build the images and create the demo user before the presentation, following the README. Stop any other stack using ports 3000 and 5001. Use commands for the same Compose project throughout the demo.

```powershell
docker compose ps
docker compose exec -T backend python -m unittest discover -s tests -v
docker compose stats --no-stream
```

Show three healthy services. Log in, open the profile and save a visible name change. Note what was saved. If using the recorded test database, Activity also contains the test wash.

```powershell
docker compose down
docker compose up -d --wait --wait-timeout 180
```

Log in again and show the saved profile value. Explain that the containers were removed and recreated, while the database volume was retained. Do not use `-v`.

The recorded verification used project `washworld-ola-test` with a separate env file and volume. Plain `docker compose` targets the default project, so use the default README setup for this sequence or explicitly select the test project's file, env file and name for every command.

## 8–10 minutes: evidence and reflection

Open `TEST_STATUS.md` and explain what the results demonstrate:

- Docker builds, frontend lint and startup passed.
- All 19 backend unit tests passed; they use mocks.
- 16 real-database integration checks passed before recreation, and 14 checks passed afterward.
- Login/profile worked through the browser, and user/profile/wash-history data survived `down`/`up` without `-v`.
- Recorded RAM usage was about 42 MiB for the frontend, 43 MiB for the backend and 65 MiB for MariaDB. These are dated snapshots after ordinary use, not a load test. Show a fresh `stats` sample if possible.
- The frontend runtime image was about 81 MiB versus 263 MiB for its build stage in the recorded measurement.

Identify an actual limitation: default signup cannot deliver verification emails until SMTP/Brevo is configured; actual mail delivery and Cypress are not verified; the engine is not rootless. Describe the implemented non-root app protections precisely.

The presentation is a ten-minute group presentation on Teams. Check the booking and submit the repository link/README as required before the 9 October deadline. Slides are optional; the repository, terminal and browser can provide the demonstration.
