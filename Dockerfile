# Use a specific Ruby version
FROM ruby:3.2-slim

# Install dependencies for Jekyll
RUN apt-get update && apt-get install -y \
    build-essential \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /usr/src/app

# Copy dependency files first (for caching)
COPY Gemfile* ./
RUN bundle install

# Copy the rest of the site code
COPY . .

# Jekyll runs on 4000 by default
EXPOSE 4000

# Commands to run the server
CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0"]
