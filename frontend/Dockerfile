# pull official base image
FROM node:16-alpine

# set working directory
WORKDIR /app

# Copies package.json and package-lock.json to Docker environment
COPY package*.json /app/

# Installs all node packages
RUN npm install

# Copies everything over to Docker environment
COPY . /app

# Port used by the application
EXPOSE 3000

# Run application
CMD ["npm", "run", "start_docker_dev"]
