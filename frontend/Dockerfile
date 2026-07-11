FROM node:20-alpine

WORKDIR /app

# 复制依赖文件
COPY package.json package-lock.json* ./
RUN npm ci

# 复制应用代码
COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
