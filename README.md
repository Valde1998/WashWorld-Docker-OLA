# WashWorld with Docker

WashWorld is a car wash app with login, memberships, wash locations and wash history. This is the Docker version of [WashWorldValde](https://github.com/Valde1998/WashWorldValde) for the OLA in Development Environments.

The idea is to run the frontend, backend and database together without installing each one separately.

## Getting started

You'll need Git and Docker Desktop running with Linux containers. These commands are for PowerShell:

```powershell
git clone https://github.com/Valde1998/WashWorld-Docker-OLA.git
cd WashWorld-Docker-OLA
Copy-Item .env.example .env
```

Open `.env` and replace `DB_ROOT_PASSWORD`, `DB_PASSWORD` and `JWT_SECRET_KEY` with three different, long, random values. The JWT key needs at least 32 characters. Keep this file on your computer, not on GitHub.

Then run:

```powershell
docker compose up --build -d --wait --wait-timeout 180
```

Once it's ready, open [localhost:3000](http://localhost:3000). The first build takes a little longer because Docker has to download the images and install the packages. Ports 3000 and 5001 need to be free. The command uses Docker Compose v2 with support for `--wait`.

## How the Docker setup works

There are three main containers: Next.js for the frontend, Flask for the backend and MariaDB for the database. The browser talks to the backend on port 5001. The backend uses `mariadb` as the database address, since `localhost` would point back to its own container.

The frontend and backend share the `web` network. Only the backend and database use the internal `data` network during normal startup. The database port isn't exposed on the computer.

MariaDB saves its data in the `cleanwash_data` volume. Removing a container doesn't remove that volume. Health checks also make the backend wait for the database to be ready before it starts.

The frontend Dockerfile uses separate build stages, so the final image only gets the files needed to run the app. The backend uses a slim Python image and Gunicorn. Both apps run without root, and the backend doesn't use the database root account. CPU and memory limits are set in Compose, and `.dockerignore` keeps local packages and `.env` out of the images.

## Trying it out

Signup normally sends a verification email. Email delivery isn't configured by default, so there's a small script for creating a local demo user:

```powershell
docker compose exec backend python demo_user.py
```

Choose a password with at least 8 characters, then log in with `demo@washworld.invalid`. The password is hashed, and the script won't overwrite an existing demo account. Normal signup still needs SMTP or Brevo settings in `.env`.

These commands show the container status, run the backend tests and show CPU and memory use:

```powershell
docker compose ps
docker compose exec -T backend python -m unittest discover -s tests -v
docker compose stats --no-stream
```

You can also open [localhost:5001/health/ready](http://localhost:5001/health/ready) to check the backend's database connection.

To check the volume, log in with the demo user first. Then remove and start the containers again:

```powershell
docker compose down
docker compose up -d --wait --wait-timeout 180
```

The same user should still be able to log in. Don't add `-v` to `docker compose down`, as that deletes the database volume too.

## A few things to keep in mind

If startup fails, check `docker compose logs --tail=100 backend mariadb frontend`.

The SQL setup files only run when the database volume is empty. Don't run `init.sql` manually on existing data: it drops tables. Changing passwords in `.env` won't update an already-created database either.

If you change `NEXT_PUBLIC_API_URL`, rebuild the frontend with the startup command above. Optional phpMyAdmin can be started with `docker compose --profile tools up -d phpmyadmin`. It's at [localhost:8080](http://localhost:8080), using `washworld` and the `DB_PASSWORD` from `.env`.

This is a local school demo, not a production setup. The full Docker setup still needs testing because Docker isn't installed on this computer. The checks already run are listed in [TEST_STATUS.md](TEST_STATUS.md), and [PRESENTATION.md](PRESENTATION.md) has notes for the demo.
