FROM python:3.12

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    awscli \
    && rm -rf /var/lib/apt/lists/*

# install node
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g aws-cdk@latest \
    && rm -rf /var/lib/apt/lists/*

# install python dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*
