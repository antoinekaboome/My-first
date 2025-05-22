# Stock Management Application

This repository contains a minimal stock management application using **CodeIgniter 4** for the backend and **React + TypeScript** for the frontend. The project is containerised with Docker and includes a GitHub Actions workflow for CI.

## Structure

- `backend/` – CodeIgniter 4 API
- `frontend/` – React application
- `docker-compose.yml` – orchestration for development
- `.github/workflows/ci.yml` – sample workflow

## Usage

1. Copy `.env.example` to `.env` and adjust database credentials.
2. From the `backend` directory run `composer install` to pull in CodeIgniter.
3. Run `docker-compose up --build` to start the stack.
4. Access the frontend at `http://localhost:3000` and the API at `http://localhost:8080`.

This is a starter template and not production ready. Security hardening, additional features, and tests should be implemented before use.


