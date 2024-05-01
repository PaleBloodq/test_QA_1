FROM node:alpine
ENV NODE_OPTIONS="--max-old-space-size=4096"

WORKDIR /frontend

COPY . .

RUN npm install

RUN npx vite build

RUN npm install -g serve
