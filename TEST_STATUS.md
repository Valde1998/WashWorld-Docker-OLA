# Test status

8 October 2026.

Checked locally:

- Backend: all 19 unit tests pass.
- Frontend: lint and build pass. These were run in the local copy with the same frontend code and Next.js configuration.
- The Compose file's YAML and structure match the official Compose schema.
- The frontend home page, logo and image display in the browser without Docker.

Docker is not installed on this computer. The following have not been tested:

- Building Docker images and starting the containers.
- Database startup, login with the database and keeping data after restarting the containers.

The existing Cypress tests have not been run either.

The unit tests use a mock database. They do not prove that the whole app works with MariaDB. The frontend preview does not have a running backend either.

Run the Docker commands and the data persistence test in the README before submission. Only mark a check as passed after it has actually been run.
