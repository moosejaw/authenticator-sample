FROM node:12.18
WORKDIR /home/node/app

RUN apt-get install -y git

RUN git clone https://github.com/dantame/interview-authentication-service .
RUN npm install

USER node
CMD ["npm", "start"]