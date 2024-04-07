FROM node:20.12.1-alpine
WORKDIR /app
COPY package.json .
RUN npm install --no-audit
COPY . .
RUN npm run build
EXPOSE 8080
CMD [ "npm", "run", "host"]