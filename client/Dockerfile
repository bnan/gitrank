FROM node:alpine as build
WORKDIR /app
ADD package.json /app
RUN npm install
ADD . /app
RUN ls
CMD ["npm", "run", "build"]

FROM nginx:alpine
RUN ls
COPY --from=build /app/build/ /usr/share/nginx/html
