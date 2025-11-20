# 🧘‍♀️ Mind Healer - 心靈處方籤 AI 諮詢系統

基於 RAG (檢索增強生成) 技術的全棧 AI 心靈諮詢應用，結合聖嚴法師《真正的快樂》智慧，提供個性化心靈建議。

## 📝 ABSTRACT

Mind Healer 是一個創新的 AI 驅動心靈諮詢系統，採用 Retrieval-Augmented Generation (RAG) 架構，結合傳統心靈智慧與現代大型語言模型技術。系統以 Vue 3 (TypeScript) 構建響應式前端介面，FastAPI 提供高效能後端服務，支援多種免費 LLM 提供商（Google Gemini 2.5、Groq、Ollama）。核心功能包含：(1) 從聖嚴法師著作中檢索相關智慧內容；(2) 隨機抽取心靈處方籤；(3) 使用 LangChain 框架整合知識庫與 LLM 生成個性化建議。技術特色在於無需昂貴的 OpenAI API，優先使用 Google Gemini 免費額度（每日 1500 次請求），並實現文本直接載入策略以規避 embedding 配額限制。系統支援 Docker 容器化部署，提供完整的開發與生產環境配置，實現了傳統心靈諮詢的數位化轉型與普及化應用。

## ✨ 核心特色

- 🤖 **多 LLM 支援**: 優先使用 Google Gemini 2.5 Flash（免費）→ Groq → Ollama → OpenAI
- 📚 **智慧 RAG**: 從聖嚴法師《真正的快樂》中檢索相關內容
- 🎲 **隨機處方籤**: 結合傳統抽籤智慧與現代 AI 技術
- 🚀 **無 Embedding 限制**: 直接文本載入策略，避免 API 配額問題
- 🐳 **容器化部署**: 完整 Docker + Docker Compose 支援
- 💰 **零成本運行**: 完全使用免費 LLM 方案

## 📁 專案結構

```
mind-healer/
├── backend/                 # FastAPI 後端
│   ├── main.py             # FastAPI 應用入口
│   ├── rag_core.py         # RAG 核心邏輯 (需要你實作)
│   ├── requirements.txt    # Python 依賴
│   └── Dockerfile          # 後端 Docker 配置
├── frontend/               # Vue 3 前端
│   ├── src/
│   │   ├── App.vue        # 主應用元件
│   │   ├── main.ts        # 應用入口
│   │   └── style.css      # 全域樣式
│   ├── package.json       # Node.js 依賴
│   ├── vite.config.ts     # Vite 配置
│   ├── Dockerfile         # 前端 Docker 配置
│   └── nginx.conf         # Nginx 配置
├── docker-compose.yaml    # Docker Compose 配置
└── README.md              # 專案說明
```

## 🚀 快速開始

### 方式 1: 使用 Docker (推薦)

1. **確保已安裝 Docker 和 Docker Compose**

2. **啟動所有服務**
   ```bash
   docker-compose up --build
   ```

3. **訪問應用**
   - 前端: http://localhost (port 80)
   - 後端 API: http://localhost:8000
   - API 文檔: http://localhost:8000/docs

### 方式 2: 本地開發

#### 後端設置

```bash
cd backend

# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安裝依賴
pip install -r requirements.txt

# 啟動後端
python main.py
```

後端將在 http://localhost:8000 運行

#### 前端設置

```bash
cd frontend

# 安裝依賴
npm install

# 啟動開發伺服器
npm run dev
```

前端將在 http://localhost:5173 運行

## ✅ RAG 系統完整實現

完整的 RAG 邏輯已實現於 `backend/rag_core.py`，包含：

## 🆓 免費 LLM 支援

本專案支援多種免費 LLM 提供商：

- ✅ **Google Gemini 2.5** - 免費額度最大（每日 1500 次）**推薦**
- ✅ **Groq** - 免費且超快（每分鐘 30 次）
- ✅ **Ollama** - 完全免費，本地運行
- ✅ **OpenAI** - 付費但效果最好

系統自動檢測可用的 LLM，優先使用 Gemini。詳見 [免費 LLM 使用指南](FREE_LLM_GUIDE.md)

## 📚 準備資料（重要！）

在啟動專案前，你需要準備文字資料。請參考 [DATA_SETUP.md](DATA_SETUP.md) 了解詳細步驟。

### 快速開始（使用 Groq - 免費）

1. **下載資料** (在專案根目錄執行)
   ```bash
   # 下載 books.zip
   curl -L -o books.zip https://github.com/yenlung/AI-Demo/raw/refs/heads/master/books.zip
   
   # 解壓縮
   unzip books.zip
   ```

2. **取得免費 Groq API Key**
   - 訪問 https://console.groq.com/keys
   - 註冊並建立 API Key（免費）
   - 複製 API Key（格式：gsk_...）

3. **設定 API Key**
   ```bash
   cd backend
   cp .env.example .env
   # 編輯 .env，填入 GROQ_API_KEY=gsk_your_key_here
   ```

4. **安裝 Groq 套件**
   ```bash
   pip install langchain-groq
   ```

5. **啟動專案**
   ```bash
   # 回到專案根目錄
   cd ..
   docker-compose up --build
   ```

### 💡 其他 LLM 選項

- **Ollama (本地免費)**：安裝 Ollama 並下載模型即可，不需要 API Key
- **OpenAI (付費)**：設定 `OPENAI_API_KEY=sk_...`

詳見 [FREE_LLM_GUIDE.md](FREE_LLM_GUIDE.md)

### 不想準備資料？

系統提供備用模式，即使沒有資料也能運行。但 RAG 功能會受限。

---

## 🔧 ~~整合你的 RAG 邏輯~~ (已完成)

### ~~步驟 1: 修改 `backend/rag_core.py`~~ ✅

~~將你 Notebook 中的 RAG 邏輯封裝到 `get_ai_response` 函式中:~~

核心功能實現：

- ✅ 書籍文本直接載入（避免 embedding 配額限制）
- ✅ 隨機心靈處方籤抽取系統
- ✅ LangChain 整合多種 LLM
- ✅ Google Gemini 2.5 Flash 生成回應
- ✅ 自動 LLM fallback 機制
- ✅ 備用模式（無資料或 API 失效時）

---

## 🔧 設置環境變數

在 `backend/` 目錄下建立 `.env` 檔案:

```env
OPENAI_API_KEY=your_api_key_here
```

並在 `docker-compose.yaml` 中添加環境變數:

```yaml
services:
  backend:
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
```

## 📡 API 端點

### POST `/api/chat`

提交使用者問題並獲取回應。

**請求:**
```json
{
  "question": "我最近工作壓力很大,該怎麼辦?"
}
```

**回應:**
```json
{
  "prescription": "天機不可洩漏,但心誠則靈。\n困境之中見真章,柳暗花明又一村。",
  "advice": "根據你的煩惱...(AI 生成的建議)"
}
```

## 🛠️ 技術棧

### 後端
- **FastAPI**: 現代、高效能的 Python Web 框架
- **Pydantic**: 資料驗證
- **Uvicorn**: ASGI 伺服器

### 前端
- **Vue 3**: 漸進式 JavaScript 框架
- **TypeScript**: 型別安全
- **Vite**: 快速的建置工具
- **Axios**: HTTP 客戶端

### 部署
- **Docker**: 容器化
- **Docker Compose**: 多容器編排
- **Nginx**: 靜態文件伺服器

## 📝 開發建議

1. **CORS 已配置**: 前端可以順利呼叫後端 API
2. **熱重載**: 本地開發時,前後端都支援熱重載
3. **錯誤處理**: 已實作基本的錯誤處理和載入狀態
4. **響應式設計**: UI 支援行動裝置和桌面裝置

## 🐛 除錯

### 檢查後端狀態
```bash
curl http://localhost:8000/
```

### 檢查 Docker 容器日誌
```bash
docker-compose logs backend
docker-compose logs frontend
```

### 停止服務
```bash
docker-compose down
```

### 重新建置
```bash
docker-compose up --build --force-recreate
```

## 📦 部署到生產環境

1. 修改 `docker-compose.yaml` 移除 volume 掛載
2. 設置環境變數 (使用 `.env` 文件或環境配置)
3. 配置 HTTPS (建議使用 Nginx + Let's Encrypt)
4. 使用 `docker-compose up -d` 在背景運行

## 📄 授權

MIT License

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request!

---

Built with ❤️ using Vue 3, FastAPI, and RAG Technology
