FROM node:18-alpine
 
WORKDIR /frontend

COPY . .

COPY ./frontend/package.json ./
 
RUN npm cache clean --force

RUN npm install

EXPOSE 5173
 
# RUN npm run build
# CMD ["npm", "start"]
CMD ["npm", "run", "dev", "--", "--host"]