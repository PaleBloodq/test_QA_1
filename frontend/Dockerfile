FROM node:alpine
ENV NODE_OPTIONS="--max-old-space-size=4096"

COPY /local.env /frontend/.env.production
WORKDIR /frontend

COPY frontend .

RUN npm install
RUN npx vite build

RUN npm install -g serve
