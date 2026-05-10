# Fullstack App (Frontend + Backend + PostgreSQL + Nginx)

This repository is prepared for university lab deployment on a single DigitalOcean Droplet using Docker Compose.

## Architecture

Containers:

1. `frontend` (Vite React app served on port `3000` inside container)
2. `backend` (Flask API on port `5000`)
3. `postgres` (`postgres:15` with persistent volume)
4. `nginx` (`nginx:alpine` reverse proxy on port `80`)

Routing:

- `/` -> `frontend:3000`
- `/api` -> `backend:5000`

## Repository Structure

```text
.
├── backend
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── test_app.py
├── frontend
│   ├── src
│   ├── Dockerfile
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml
├── nginx.conf
└── .github/workflows
    ├── ci.yml
    └── deploy.yml
```

## Local Setup (without Docker)

### Backend

```bash
cd backend
python -m pip install -r requirements.txt
export DATABASE_URL='postgresql://postgres:mypassword@localhost:5432/mydb'
export DB_SSLMODE=disable
python app.py
```

Backend runs on `http://localhost:5000`.

Health endpoint:

```bash
curl http://localhost:5000/api/health
```

### Frontend

```bash
cd frontend
npm install
npm run build
npm start
```

Frontend runs on `http://localhost:3000`.

## Docker Setup

### Start all services

```bash
docker-compose up -d --build
```

### Check running services

```bash
docker-compose ps
docker-compose logs -f
```

### Stop services

```bash
docker-compose down
```

### Stop and remove volumes (deletes PostgreSQL data)

```bash
docker-compose down -v
```

## DigitalOcean Deployment (One Droplet)

1. Create one Ubuntu Droplet.
2. Install Docker + Docker Compose on the Droplet.
3. Clone this repository on the Droplet (example path: `/root/fullstack-app`).
4. Ensure firewall allows inbound `80`.
5. Push to `main` branch (or manually run deploy commands below).

Manual deploy commands on Droplet:

```bash
cd /root/fullstack-app
git pull origin main
docker-compose up -d --build
```

## GitHub Actions Deployment Workflow

Workflow file: `.github/workflows/deploy.yml`

It deploys via SSH to the droplet and runs:

```bash
git pull origin main
docker-compose up -d --build
```

### Required GitHub Secrets

Set these in repository settings -> **Secrets and variables** -> **Actions**:

- `SERVER_IP` (Droplet public IP)
- `SERVER_USER` (SSH user, e.g. `root`)
- `SERVER_PORT` (usually `22`)
- `SSH_PRIVATE_KEY` (private key matching droplet authorized key)
- `APP_PATH` (absolute path to project on server, e.g. `/root/fullstack-app`)

## Useful Docker Commands

```bash
# Rebuild a single service
docker-compose build frontend

# Restart a single service
docker-compose restart backend

# View logs for one service
docker-compose logs -f nginx

# Execute command in container
docker-compose exec backend python -V
```

## Health Checks

Configured in `docker-compose.yml`:

- `postgres`: `pg_isready`
- `backend`: checks `http://localhost:5000/api/health`
- `frontend`: checks `http://localhost:3000`
- `nginx`: checks `http://localhost/`

## Troubleshooting

### 1) `React is not defined`

- Ensure frontend was rebuilt:
  ```bash
  docker-compose build frontend
  docker-compose up -d frontend
  ```

### 2) Backend cannot connect to database

- Check `DATABASE_URL` in `docker-compose.yml`.
- Ensure postgres is healthy:
  ```bash
  docker-compose ps
  docker-compose logs postgres
  ```

### 3) Nginx returns 502/504

- Verify backend/frontend containers are healthy:
  ```bash
  docker-compose ps
  docker-compose logs nginx
  docker-compose logs backend
  docker-compose logs frontend
  ```

### 4) Deployment workflow fails

- Verify all required GitHub secrets exist and are correct.
- Confirm SSH key works for `SERVER_USER@SERVER_IP`.
- Check server path in `APP_PATH`.

### 5) Port 80 not reachable

- Confirm droplet firewall/cloud firewall allows TCP `80`.
- Check nginx service status:
  ```bash
  docker-compose ps nginx
  docker-compose logs nginx
  ```
