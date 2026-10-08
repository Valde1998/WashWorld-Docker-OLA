# WashWorld with Docker

WashWorld is a car wash app with login, memberships, wash locations and wash history. This is the Docker version of [WashWorldValde](https://github.com/Valde1998/WashWorldValde) for the OLA in Development Environments.

Docker Compose runs the frontend, backend and database together without installing each one separately. The Docker build, startup, login and database persistence were tested on 8 October 2026. See [TEST_STATUS.md](TEST_STATUS.md) for the results, measurements and remaining limitations.

## Getting started

You'll need Git and Docker Desktop running with Linux containers. Use Docker Compose with support for `--wait`; the recorded test used Compose v5.1.3. Ports 3000 and 5001 need to be free. These commands are for PowerShell:

```powershell
git clone https://github.com/Valde1998/WashWorld-Docker-OLA.git
cd WashWorld-Docker-OLA
Copy-Item .env.example .env
```

Open `.env` and replace `DB_ROOT_PASSWORD`, `DB_PASSWORD` and `JWT_SECRET_KEY` with three different, long, random values. The JWT key needs at least 32 characters. Keep this file on your computer, not on GitHub.

Then run:

```powershell
docker compose config --quiet
docker compose up --build -d --wait --wait-timeout 180
docker compose ps
```

All three main services should become `healthy`. Open [localhost:3000](http://localhost:3000). The first build takes longer because Docker downloads images and installs packages.

## How the Docker setup works

[docker-compose.yml](docker-compose.yml) defines three main services: Next.js for the frontend, Flask for the backend and MariaDB for the database. The browser reaches the frontend on host port 3000 and calls the backend on host port 5001. Both ports are published only on `127.0.0.1`.

The frontend and backend share the named `web` network. The backend and database share the internal named `data` network. The backend uses `mariadb:3306` as the database address; `localhost` inside a container would point back to that container. MariaDB has no published host port.

MariaDB saves its data in the named `cleanwash_data` volume at `/var/lib/mysql`. Compose prefixes the actual network and volume names with its project name. Normal startup uses `washworld-ola`; the recorded test used a separate `washworld-ola-test` project and a fresh volume.

The SQL initialization files are mounted read-only and run only when the database volume is empty. Readiness checks make the backend wait for MariaDB, and the frontend wait for the backend. The backend's `/health/ready` endpoint runs a real database query.

### Build stages and security choices

[frontend/Dockerfile](frontend/Dockerfile) has dependencies, build and runtime stages. `npm ci` installs the lockfile's packages; the build stage compiles Next.js; the runtime stage gets the standalone server, static files and public assets. Development packages stay out of the runtime image. `NEXT_PUBLIC_API_URL` is set at build time because browser code needs it.

[backend/Dockerfile](backend/Dockerfile) has dependencies and runtime stages. Dependencies are installed separately, then copied into a slim Python runtime that starts the app with Gunicorn. Copying the package manifests before the app code lets Docker reuse dependency layers when only the app code changes. `.dockerignore` keeps local packages and `.env` out of the build context.

The frontend app process runs as `node` (UID 1000), and the backend as `app` (UID 10001). Both appservices drop all Linux capabilities and set `no-new-privileges`. The backend uses the `washworld` database user, not DB-root. Its database privileges are SELECT, INSERT, UPDATE, DELETE and CREATE on `cleanwash.*`; CREATE supports application startup.

These are verified non-root application processes. **The tested Docker Desktop engine does not run in rootless mode.** A Dockerfile `USER` instruction alone does not make the engine rootless or establish that an entire deployment is secure.

Compose limits frontend and backend to 512 MiB RAM and one CPU each; MariaDB has 768 MiB and one CPU. These are limits, not the amount of memory the services always use. Actual measurements and image sizes are in [TEST_STATUS.md](TEST_STATUS.md).

## Trying it out

Signup normally sends a verification email. Email delivery isn't configured by default, so create a local demo user:

```powershell
docker compose exec backend python demo_user.py
```

Choose a password with at least 8 characters, then log in with `demo@washworld.invalid`. The password is hashed, and the script won't overwrite an existing demo account. Normal signup needs SMTP or Brevo settings in `.env`.

Log in, view the membership and wash locations, and save a profile change. These commands check container status, run the backend tests and show CPU and memory use:

```powershell
docker compose ps
docker compose exec -T backend python -m unittest discover -s tests -v
docker compose stats --no-stream
```

Open [localhost:5001/health/ready](http://localhost:5001/health/ready) to check the backend's database connection. The unit tests use mocks, so they are separate from the recorded integration checks against MariaDB.

### Check persistence and stop the app

First log in and save a profile change. Note the name or number plate you saved. Then remove and start the containers again:

```powershell
docker compose down
docker compose up -d --wait --wait-timeout 180
```

Log in with the same user and check that your profile change is still there. In the recorded test, the user, profile change and a wash-history entry survived this sequence.

Use `docker compose down` to stop and remove the containers and networks while keeping the named database volume. **Do not add `-v` if you need the data:** it removes the named volume too.

## Troubleshooting and limitations

If startup fails, check `docker compose logs --tail=100 backend mariadb frontend`. Confirm that Docker Desktop is running and that ports 3000 and 5001 are free. Only one stack can use these host ports at a time, including a separately named test stack.

The SQL setup files only run when the database volume is empty. Don't run `init.sql` manually on existing data: it drops tables. Changing passwords in `.env` won't update an already-created database either.

If you change `NEXT_PUBLIC_API_URL`, rebuild the frontend with the startup command above. Optional phpMyAdmin can be started with `docker compose --profile tools up -d phpmyadmin`. It's at [localhost:8080](http://localhost:8080), using `washworld` and the `DB_PASSWORD` from `.env`. This optional service was not part of the recorded test.

This is a local school demo. Actual email delivery and the complete email-verification/password-reset flows have not been tested, and the existing Cypress tests have not been run. There is no source-code bind mount for hot reload; the recorded volume test demonstrates database persistence. The non-root apps run on a Docker engine that is not rootless. See [TEST_STATUS.md](TEST_STATUS.md) for the full test scope and [PRESENTATION.md](PRESENTATION.md) for the demo sequence.
