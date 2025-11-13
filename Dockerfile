FROM node:20-alpine

WORKDIR /app

# Installer seulement les deps Node
COPY package.json ./
RUN npm install --production

# Copier le code
COPY server.mjs tools.mjs ./

EXPOSE 8787
CMD ["node", "server.mjs"]
