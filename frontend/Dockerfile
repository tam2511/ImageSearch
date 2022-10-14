FROM node:16.15.0 AS builder

WORKDIR /server
COPY package.json package.json
COPY package-lock.json package-lock.json
COPY .prettierrc.json .prettierrc.json
COPY favicon.svg favicon.svg
COPY tsconfig.json tsconfig.json
COPY vite.config.js vite.config.js
COPY src src
COPY index.html index.html

RUN npm install
RUN npm run build

FROM nginx:latest

RUN rm -rf /etc/nginx/conf.d/default.conf
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

# Static build
COPY --from=builder /server/dist /usr/share/nginx/html

RUN mkdir /usr/share/nginx/html/public

# Set working directory
WORKDIR /usr/share/nginx/html

# Start Nginx server
CMD ["/bin/bash", "-c", "nginx -g \"daemon off;\""]
