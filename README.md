# WashWorld – Docker OLA

WashWorld is a car wash app with memberships, locations and wash history, based on [WashWorldValde](https://github.com/Valde1998/WashWorldValde). For this OLA, the existing app runs with Docker Compose so the frontend, backend and database can start together.

## Run the project

You need Git and Docker Desktop with Linux containers. Start Docker Desktop and make sure ports 3000 and 5001 are available.

For a fresh checkout in PowerShell:

```powershell
git clone https://github.com/Valde1998/WashWorld-Docker-OLA.git
cd WashWorld-Docker-OLA
Copy-Item .env.example .env
```

Set `DB_ROOT_PASSWORD`, `DB_PASSWORD` and `JWT_SECRET_KEY` in `.env` to three different, long random values. The JWT key must be at least 32 characters. `.env` is ignored by Git. If you already have a configured file, keep it.

Build and start the app from the project folder:

```powershell
docker compose up --build -d
docker compose ps
```

Wait until all three services are `healthy`, then open [localhost:3000](http://localhost:3000). The first build may take a while.

## Demo login

Email is not configured by default. Create a local demo user with:

```powershell
docker compose exec backend python demo_user.py
```

Choose a password of at least eight characters and log in with `demo@washworld.invalid`. If the account already exists, the script leaves it unchanged. Regular signup needs SMTP or Brevo to send the verification email.

## How it works

- **Frontend:** Next.js on port 3000.
- **Backend:** Flask on port 5001.
- **Database:** MariaDB, reached by the backend at `mariadb:3306`.

[docker-compose.yml](docker-compose.yml) connects the services through the `web` and `data` networks. The database port is not published to the host, and the app ports are only available on localhost. MariaDB stores its data in the `cleanwash_data` volume at `/var/lib/mysql`.

Both Dockerfiles use multi-stage builds, and the frontend/backend run as non-root users. Health checks check that services are ready. Compose also sets CPU and memory limits.

## Test and stop

Run the backend tests, view logs and check resource use:

```powershell
docker compose exec backend python -m unittest discover -s tests
docker compose logs --tail=50
docker stats --no-stream
```

To check persistence, save a profile change and then run:

```powershell
docker compose down
docker compose up -d
```

Once the services are ready, log in again and check that your change is still there. Stop the app with `docker compose down`. Leave out `-v` if you want to keep the database.

See [test results](TEST_STATUS.md) and [demo notes](PRESENTATION.md). Email flows and Cypress have not been tested. The Docker Desktop engine is not rootless; non-root app users are a separate protection. This is a limitation regarding [the assignment's mention of rootless](https://ek.itslearning.com/main.aspx?CourseID=7577&ElementID=1566430&ElementType=131072).
