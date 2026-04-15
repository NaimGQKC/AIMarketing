# Stage 1: Build frontend
FROM node:22-alpine AS frontend
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Backend + serve built frontend
FROM python:3.13-slim AS runtime
WORKDIR /app

# Install Python deps
COPY server/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY server/ ./server/

# Copy built frontend
COPY --from=frontend /app/dist ./dist/

# Serve static files from FastAPI
WORKDIR /app/server

EXPOSE 8000
CMD ["python", "main.py"]
