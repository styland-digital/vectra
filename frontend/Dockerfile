FROM node:20-alpine

# Install dependencies
RUN apk add --no-cache libc6-compat

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci || npm install

# Copy application code
COPY . .

# Disable telemetry
ENV NEXT_TELEMETRY_DISABLED 1

EXPOSE 3000

# Default command (will be overridden by docker-compose.yml for dev mode)
CMD ["npm", "run", "dev"]
