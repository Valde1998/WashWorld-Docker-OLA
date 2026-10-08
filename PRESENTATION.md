# OLA demo notes

Prepare the images and demo user before presenting. Have the README, Compose file, Dockerfiles and browser open. The presentation is a ten-minute group presentation on Teams.

## 1. Introduce the app

WashWorld has a Next.js frontend, Flask backend and MariaDB database. Docker Compose starts them together.

## 2. Show the setup

Open `docker-compose.yml` and explain the ports, `web`/`data` networks and database volume. Then show the multi-stage builds and non-root users in the Dockerfiles. Secrets are in `.env`; keep its contents private.

## 3. Show the app working

```powershell
docker compose up -d
docker compose ps
```

Once all services are healthy, log in at http://localhost:3000. Show the locations and save a profile change.

## 4. Show that data is kept

```powershell
docker compose down
docker compose up -d
```

Wait for healthy services, log in again and show the saved change. Explain that the containers were recreated while the database volume was kept. Do not use `-v`.

## 5. Tests and limitations

```powershell
docker compose exec backend python -m unittest discover -s tests
docker stats --no-stream
```

Use [TEST_STATUS.md](TEST_STATUS.md) to explain the results. Stats shows a snapshot of CPU and memory use, not a load test.

Email is not configured, and Cypress has not been tested. The app processes are non-root, but the Docker Desktop engine is not rootless. Explain this difference accurately: rootless is mentioned in the assignment and is not part of this simpler setup.

Remember to book a time and submit the repository link and README as instructed.
