FROM node:latest
ENV NODE_OPTIONS="--max-old-space-size=4096"

WORKDIR /frontend

COPY . frontend/

RUN npm --prefix frontend/ install

RUN npx vite build

RUN npm install -g serve
