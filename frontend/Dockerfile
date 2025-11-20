FROM node:20-alpine as build

WORKDIR /app

# 複製 package files
COPY package*.json ./

# 安裝依賴
RUN npm install

# 複製原始碼
COPY . .

# 建置應用程式
RUN npm run build

# 使用 nginx 提供靜態文件
FROM nginx:alpine

# 複製建置結果到 nginx
COPY --from=build /app/dist /usr/share/nginx/html

# 複製 nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
