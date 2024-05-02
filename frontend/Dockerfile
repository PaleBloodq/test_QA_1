FROM node:alpine
ENV NODE_OPTIONS="--max-old-space-size=4096"


WORKDIR /frontend

COPY . .
RUN echo "VITE_BASE_URL=${VITE_BASE_URL}" >> .env.production && \
    echo "VITE_API_URL=${VITE_API_URL}" >> .env.production

RUN npm install
RUN npx vite build

RUN npm install -g serve
