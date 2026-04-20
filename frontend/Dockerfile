FROM node:20-alpine AS build
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend /app
ARG VITE_API_URL=http://backend:8000
ENV VITE_API_URL=${VITE_API_URL}
RUN npm run build

FROM node:20-alpine
WORKDIR /app
RUN npm install -g vite
COPY --from=build /app/dist ./dist
COPY frontend/package.json ./package.json
EXPOSE 5173
CMD ["vite", "preview", "--host", "0.0.0.0", "--port", "5173", "--strictPort"]
