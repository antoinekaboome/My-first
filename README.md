# Stock Management Application

This repository contains a minimal stock management application using **PHP** for the backend and **React + TypeScript** for the frontend. The project is containerised with Docker and includes a GitHub Actions workflow for CI.

## Structure

- `backend/` – PHP API with simple routing
- `frontend/` – React application
- `docker-compose.yml` – orchestration for development
- `.github/workflows/ci.yml` – sample workflow

## Usage

1. Copy `.env.example` to `.env` and adjust database credentials.
2. Run `docker-compose up --build` to start the stack.
3. Access the frontend at `http://localhost:3000` and the API at `http://localhost:8080`.

This is a starter template and not production ready. Security hardening, additional features, and tests should be implemented before use.


