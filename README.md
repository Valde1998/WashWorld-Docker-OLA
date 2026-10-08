# WashWorld – Docker OLA

WashWorld is a car wash app with memberships, locations and wash history. It is based on [WashWorldValde](https://github.com/Valde1998/WashWorldValde). For this project, Docker Compose starts the existing frontend, backend and database together.

## Run the project

You need Git and Docker Desktop with Linux containers. Start Docker Desktop and make sure ports 3000 and 5001 are available.

From PowerShell:

```powershell
git clone https://github.com/Valde1998/WashWorld-Docker-OLA.git
cd WashWorld-Docker-OLA
Copy-Item .env.example .env
```

Set `DB_ROOT_PASSWORD`, `DB_PASSWORD` and `JWT_SECRET_KEY` in `.env` to different, long random values. The JWT key must be at least 32 characters. Keep an existing configured `.env`; this file is ignored by Git.

```powershell
docker compose up --build -d
docker compose ps
```

Wait until all three services are `healthy`, then open [localhost:3000](http://localhost:3000). The first build can take a while.

Email is not configured by default, so create a local demo user:

```powershell
docker compose exec backend python demo_user.py
```

Choose a password of at least eight characters and log in with `demo@washworld.invalid`. An existing demo account is kept unchanged. Regular signup needs SMTP or Brevo for verification emails.

## How it works

- Next.js serves the frontend on port 3000.
- The frontend calls the Flask API on port 5001.
- Flask reads and writes data in MariaDB at `mariadb:3306`.

[docker-compose.yml](docker-compose.yml) connects the services using the `web` and `data` networks. Only the app ports are published, both on localhost. The database uses the `cleanwash_data` volume at `/var/lib/mysql` to keep its data.

The [frontend Dockerfile](frontend/Dockerfile) and [backend Dockerfile](backend/Dockerfile) use multi-stage builds and non-root app users. Compose adds health checks and CPU/memory limits.

## Check and stop

```powershell
docker compose exec backend python -m unittest discover -s tests
docker compose logs --tail=50
docker stats --no-stream
```

To check persistence, log in and save a profile change, then recreate the containers:

```powershell
docker compose down
docker compose up -d
```

Wait for healthy services, log in again and check that the change is still there. Stop with `docker compose down`. Do not add `-v` if you want to keep the database.

Tested on 8 October 2026: all 19 backend unit tests passed using mocks. Checks with the real database also passed: 20 before and 16 after recreating containers. These covered login, profiles, wash history and validation. Saved data survived the restart.

At 14:57 CEST after these checks, Compose stats showed roughly 33 MiB for the frontend, 42 MiB for the backend and 60 MiB for MariaDB. This was a snapshot, not a load test.

For the presentation, show the Compose file and Dockerfiles, demonstrate a profile change surviving a restart, and explain the test results.

## Limitations

Email flows and Cypress have not been tested. The Docker Desktop engine is not rootless, although the app processes run as non-root users. Rootless is mentioned in the [assignment](https://ek.itslearning.com/main.aspx?CourseID=7577&ElementID=1566430&ElementType=131072), so this remains a limitation of this setup.
