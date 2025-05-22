FROM node:18-alpine as build
WORKDIR /app
COPY package.json tsconfig.json ./
COPY src ./src
RUN npm install && npm run build

FROM node:18-alpine
WORKDIR /app
COPY package.json ./
RUN npm install --only=production
COPY --from=build /app/dist ./dist
CMD ["node", "dist/server.js"]
