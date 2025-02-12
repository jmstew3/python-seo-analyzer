# Use Node 16 as base image
FROM node:16-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Add host binding for React development server
ENV HOST=0.0.0.0

# Expose port 3000
EXPOSE 3000

# Start the development server
CMD ["npm", "start"]
