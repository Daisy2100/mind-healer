# Mind Healer Backend Docker Package

後端已完整打包為 Docker 容器，可獨立部署。

## 📦 包含文件

```
backend/
├── Dockerfile              # Docker 映像定義
├── docker-compose.yml      # Docker Compose 配置
├── deploy.sh              # Linux/Mac 部署腳本
├── deploy.ps1             # Windows 部署腳本
├── requirements.txt       # Python 依賴
├── .env.example          # 環境變數範本
├── main.py               # FastAPI 入口
├── rag_core.py           # RAG 核心邏輯
└── books/                # 文本數據目錄
```

## 🚀 快速部署

### Windows 用戶

```powershell
cd backend
.\deploy.ps1
```

### Linux/Mac 用戶

```bash
cd backend
chmod +x deploy.sh
./deploy.sh
```

### 手動部署

```bash
# 1. 構建映像
docker build -t mind-healer-backend .

# 2. 運行容器
docker run -d \
  --name mind-healer-backend \
  -p 8000:8000 \
  -v $(pwd)/books:/app/books \
  --env-file .env \
  mind-healer-backend
```

## 🔧 環境配置

編輯 `.env` 文件：

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

## 📝 部署檢查清單

- [ ] Docker 已安裝並運行
- [ ] `.env` 文件已配置 API Key
- [ ] `books/` 目錄包含文本文件
- [ ] 端口 8000 未被占用

## 🌐 訪問服務

部署成功後：

- **API 端點**: http://localhost:8000
- **Swagger 文檔**: http://localhost:8000/docs
- **健康檢查**: http://localhost:8000/

## 📊 監控與日誌

```bash
# 查看日誌
docker-compose logs -f

# 查看容器狀態
docker-compose ps

# 重啟服務
docker-compose restart

# 停止服務
docker-compose down
```

## 🔄 更新部署

```bash
# 拉取最新代碼
git pull

# 重新部署
docker-compose down
docker-compose up -d --build
```

## 🐛 故障排除

### 容器無法啟動

```bash
# 查看詳細日誌
docker-compose logs backend

# 檢查映像
docker images | grep mind-healer

# 重建映像
docker-compose build --no-cache
```

### API 無法訪問

1. 檢查容器狀態：`docker ps`
2. 檢查端口：`netstat -an | findstr 8000`
3. 檢查防火牆設置

### RAG 初始化失敗

1. 確認 `.env` 中 API Key 正確
2. 確認 `books/` 目錄有文件
3. 檢查網路連接（LLM API 需要網路）

## 📖 詳細文檔

請參閱 [DEPLOYMENT.md](DEPLOYMENT.md) 獲取完整部署指南。

## 🔒 安全注意事項

- **不要**將 `.env` 文件提交到版本控制
- **不要**在公開場所暴露 API Key
- 生產環境建議使用環境變數而非 `.env` 文件
- 考慮使用 HTTPS 和反向代理（如 Nginx）

## 📞 技術支援

遇到問題？查看：

1. [DEPLOYMENT.md](DEPLOYMENT.md) - 完整部署文檔
2. [TECHNICAL_REPORT.md](../TECHNICAL_REPORT.md) - 技術實現報告
3. Docker 日誌：`docker-compose logs -f`
