# WashWorld – Docker OLA

WashWorld is a car wash app with memberships, locations and wash history, based on [WashWorldValde](https://github.com/Valde1998/WashWorldValde). Docker Compose runs its Next.js frontend, Flask backend and MariaDB database together.

## Run the project

You need Git, Docker Compose and a Linux or WSL2 environment with [Docker Engine configured in rootless mode](https://docs.docker.com/engine/security/rootless/). Use systemd and cgroup v2 for the [resource limits](https://docs.docker.com/engine/security/rootless/tips/#limiting-resources). This is already set up on this computer.

For a fresh checkout, run `git clone https://github.com/Valde1998/WashWorld-Docker-OLA.git`, then `cd WashWorld-Docker-OLA`.

On this Windows computer, open PowerShell and enter the prepared Linux environment:

```powershell
wsl -d WashWorld-OLA-Rootless -u ola --cd /mnt/c/Users/valde/Documents/WashWorld-Docker-OLA
```

Keep this terminal open while using the app. Run the following commands in Linux, from the project folder:

```bash
systemctl --user start docker
docker context use rootless
export COMPOSE_PROJECT_NAME=washworld-ola-rootless
id -u
docker info --format '{{json .SecurityOptions}}'
```

The user ID must be nonzero and the security options must include `rootless`. The project name keeps the existing rootless database on this computer. Docker Desktop uses a separate engine; stop its WashWorld containers first if they occupy ports 3000 or 5001.

For a fresh checkout, copy `.env.example` to `.env` using `cp .env.example .env`. Keep an existing configured `.env`. Set `DB_ROOT_PASSWORD`, `DB_PASSWORD` and `JWT_SECRET_KEY` to different, long random values; the JWT key needs at least 32 characters. `.env` is ignored by Git.

```bash
docker compose up --build -d
docker compose ps
```

Wait until all three services are `healthy`, then open [localhost:3000](http://localhost:3000).

Email is not configured by default. Create a local demo user with:

```bash
docker compose exec backend python demo_user.py
```

Choose a password of at least eight characters and log in with `demo@washworld.invalid`. Existing demo accounts are left unchanged. Regular signup needs SMTP or Brevo for verification emails.

## How it works

The frontend runs on port 3000 and calls Flask on port 5001. Flask reaches MariaDB at `mariadb:3306`.

[docker-compose.yml](docker-compose.yml) connects the services through the `web` and `data` networks. Only the app ports are published, both on localhost. The `cleanwash_data` volume stores the database at `/var/lib/mysql`.

The [frontend Dockerfile](frontend/Dockerfile) and [backend Dockerfile](backend/Dockerfile) use multi-stage builds and non-root app users. Rootless Docker also runs the engine without Linux host root privileges. These are two separate protections, as covered in the [class exercise](https://ek.itslearning.com/main.aspx?CourseID=7577&ElementID=1561803&ElementType=131072).

## Check and stop

In the same Linux terminal:

```bash
docker compose exec backend python -m unittest discover -s tests
docker compose logs --tail=50
docker stats --no-stream
```

To check persistence, save a profile change and recreate the containers:

```bash
docker compose down
docker compose up -d
```

Once the services are healthy, log in again and check that the change is still there. Stop with `docker compose down`. Leave out `-v` to keep the database.

Tested on 8 October 2026: 19 backend unit tests passed using mocks. Separate checks with the real database passed before and after recreating containers, including login, profile changes and saved wash history. Rootless mode, non-root app users and CPU/memory limits were also checked.

At around 16:41 CEST after these checks, Compose stats showed about 32 MiB for the frontend, 42 MiB for the backend and 60 MiB for MariaDB. This was a snapshot, not a load test.

For the presentation, show the Compose file and Dockerfiles, demonstrate persistence and explain the results. Email flows and Cypress have not been tested.
