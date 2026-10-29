# Compila o React e serve os arquivos estáticos com Caddy.
FROM node:22 AS build

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM caddy:2
COPY --from=build /app/dist /srv
