FROM node:20-bullseye
RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY package.json ./
RUN npm install --production
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY bridge.mjs mcp_server.py ./
EXPOSE 8787
CMD ["node", "bridge.mjs"]
