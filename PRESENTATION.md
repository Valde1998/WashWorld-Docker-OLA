# Presentation notes

## The project

WashWorld is a car wash app. The frontend uses Next.js, the backend uses Flask, and the data is stored in MariaDB. Docker Compose starts the parts together, so they do not need to be installed separately.

## The main Docker ideas

- An image is a package containing the app and what it needs. A container is a running instance of that image.
- Each of the three parts has its own container.
- The backend finds the database using the name `mariadb` on the internal network.
- A volume keeps the database data when the container is removed.
- The frontend is built in several stages, so the final image does not contain all the development packages.
- The frontend and backend run without root. Passwords are kept in `.env`, which is not shared on GitHub.
- Health checks check that each part is ready before the next part starts.

Show `docker-compose.yml` and the Dockerfiles while explaining them. Do not show the contents of `.env`.

## Demo

Start the app and create the demo user before the presentation, as described in the README.

```powershell
docker compose ps
docker compose exec -T backend python -m unittest discover -s tests -v
docker compose stats --no-stream
```

Open the app, log in and show the profile and wash locations. Then remove the containers with `docker compose down` and start them again. Show that the same user can still log in. Do not use `-v`.

## At the end

Explain what has actually been tested and what still needs testing. For real use on the internet, the app would also need HTTPS, backups and updated images.

The main thing is to explain images, containers, networks and volumes in your own words.
