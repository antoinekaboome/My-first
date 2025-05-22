# Inventory Management Application

This repository contains a full stack stock management application built with **Node.js/Express** and **React** (both in TypeScript). It supports secure authentication, CRUD operations for products, categories and suppliers, stock movement tracking and audit logging.

## Features

- User authentication with JWT and bcrypt password hashing
- Role based authorization (admin, employee)
- CRUD APIs for products, categories, suppliers and stock movements
- Audit log of user actions
- Dashboard highlighting low stock items
- Rate limiting, CORS and security headers
- Dockerized backend, frontend and MongoDB
- GitHub Actions workflows for CI and Docker image build

## Getting Started

Create a `.env` file in `backend` and `frontend` based on the provided `.env.example` files.

### Using Docker Compose

```bash
docker-compose up --build
```

The frontend will be available on `http://localhost:3000` and the backend API on `http://localhost:5000`.

### Development

Install dependencies (requires Node.js 18):

```bash
cd backend && npm install
cd ../frontend && npm install
```

Run the backend in dev mode:

```bash
npm run dev
```

Run the frontend:

```bash
npm start
```

## Testing

Both the frontend and backend include placeholder Jest tests which can be run with `npm test` in their respective directories.

