FROM node:20-alpine

RUN apk add --no-cache libc6-compat

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["sh", "-c", "npm run dev"]