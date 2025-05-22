FROM node:18
WORKDIR /app
COPY package.json tsconfig.json webpack.config.js ./
COPY src ./src
RUN npm install && npm run build
CMD ["npx", "http-server", "dist", "-p", "3000"]

