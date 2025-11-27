# ⚔️ 小明劍魔 AI 吐槽系統

> 「怎麼不找找自己的問題？」

基於 RAG (檢索增強生成) 技術的諷刺風格 AI 吐槽系統，用黑色幽默陪你面對人生困境。

## ⚠️ 免責聲明

**本系統為諷刺/迷因專案，僅供娛樂用途！**

靈感來源：B站實況主「小明劍魔」的經典語錄，將遊戲失敗延伸到社會現實的荒謬吐槽。

## 🗡️ 迷因背景

2025年1月31日，中國B站實況主「小明劍魔」在直播LOL七連敗後被觀眾嘲諷「怎麼不找找自己的問題」，隨後爆發一連串經典吐槽，成為網路熱門迷因：

**經典語錄：**
- 「怎麼不找找自己的問題？」
- 「我爸得了MVP，你媽就是躺贏狗！」
- 「他們不解決問題，他們解決你！」
- 「評分系統把人的付出異化掉了，懂嗎？」
- 「輸了還不能說？輸了還不能有情緒？」

## ⚔️ 劍魔語錄庫

本系統內建 7 條經典劍魔語錄：

```javascript
const swordDemonQuotes = [
  "怎麼不找找自己的問題？",
  "我爸得了MVP，你媽就是躺贏狗！",
  "他們不解決問題，他們解決你！",
  "我只能戰死，不能躺平被推死！",
  "評分系統把人的付出異化掉了，懂嗎？",
  "你太出格，你太激進！",
  "輸了還不能說？輸了還不能有情緒？"
];
```


## 參考資料

本專案參考並改進自以下開源專案：

- **原始專案**: [用 RAG 打造心靈處方籤機器人](https://github.com/yenlung/AI-Demo/blob/master/%E3%80%90Demo06%E3%80%91%E7%94%A8_RAG_%E6%89%93%E9%80%A0%E5%BF%83%E9%9D%88%E8%99%95%E6%96%B9%E7%B1%A4%E6%A9%9F%E5%99%A8%E4%BA%BA.ipynb)
- **作者**: yenlung
- **迷因來源**: B站實況主小明劍魔
- **改進內容**: 
  - 從心靈處方籤改造為諷刺吐槽系統
  - 加入劍魔語錄庫（7條經典語錄）
  - 暗黑系 UI 設計（紅黑配色）
  - 諷刺風格 AI Prompt 設計
  
**核心功能：**
1. 隨機抽取劍魔語錄
2. 用黑色幽默風格回應使用者煩惱
3. 把個人問題延伸到社會議題諷刺
4. 最後給予真正有意義的建議（諷刺包裝）

**技術特色：**
- 無需昂貴的 OpenAI API，優先使用 Google Gemini 免費額度（每日 1500 次請求）
- 諷刺風格 Prompt Engineering
- 暗黑系 UI 設計（紅黑配色、發光動畫）
- 支援 Docker 容器化部署
- 實現自動 LLM fallback 機制，確保服務穩定性

## ✨ 核心特色

- ⚔️ **劍魔語錄**: 7 條經典語錄，隨機抽取
- 🗡️ **諷刺吐槽**: 用黑色幽默風格回應煩惱
- 🌙 **暗黑 UI**: 紅黑配色的憤怒風格設計
- 🤖 **多 LLM 支援**: 自動檢測並使用可用 LLM（Gemini → Groq → Ollama → OpenAI）
- 🚀 **無 Embedding 限制**: 直接文本載入策略，避免 API 配額問題
- 🐳 **完整容器化**: 前後端獨立 Docker 部署 + 整合 Docker Compose
- 💰 **零成本運行**: 完全使用免費 LLM 方案（推薦 Google Gemini）
- 🔄 **自動降級**: LLM 不可用時自動切換備用方案

## 📁 專案結構

```plaintext
mind-healer/
├── backend/                      # FastAPI 後端
│   ├── main.py                   # FastAPI 應用入口
│   ├── rag_core.py               # RAG 核心邏輯（已完整實現）
│   ├── requirements.txt          # Python 依賴套件
│   ├── Dockerfile                # 後端 Docker 映像配置
│   ├── docker-compose.yml        # 後端獨立部署配置
│   ├── deploy.ps1                # Windows 部署腳本
│   ├── build.sh                  # Linux/Mac 建置腳本
│   ├── README.md                 # 後端部署說明
│   ├── .env                      # 環境變數配置（需自行建立）
│   └── books/                    # 文本資料目錄
│       └── book1.txt             # 聖嚴法師著作文本
├── frontend/                     # Vue 3 + TypeScript 前端
│   ├── src/
│   │   ├── App.vue               # 主應用元件
│   │   ├── main.ts               # 應用入口
│   │   ├── style.css             # 全域樣式
│   │   └── vite-env.d.ts         # TypeScript 環境定義
│   ├── package.json              # Node.js 依賴
│   ├── vite.config.ts            # Vite 建置配置
│   ├── tsconfig.json             # TypeScript 配置
│   ├── Dockerfile                # 前端 Docker 映像配置
│   ├── nginx.conf                # Nginx 反向代理配置
│   ├── deploy.ps1                # Windows 部署腳本
│   ├── .env.development          # 開發環境配置
│   └── .env.production           # 生產環境配置
├── books/                        # 共用文本資料
│   └── book1.txt
├── docker-compose.yaml           # 整合部署配置
├── setup.ps1                     # 快速設置腳本
└── README.md                     # 專案總覽（本文件）
```

## 🚀 快速開始

### 方式 1: 一鍵快速設置（推薦新手）

使用自動化設置腳本，自動下載資料、配置環境、啟動服務：

```powershell
.\setup.ps1
```

腳本將自動：

1. 下載聖嚴法師《真正的快樂》書籍資料
2. 引導設置 LLM API Key（支援 Gemini/Groq/Ollama/OpenAI）
3. 選擇啟動模式（Docker 或本地開發）

### 方式 2: 後端獨立部署

後端已完整打包為 Docker 容器，可獨立部署：

**Windows 用戶：**

```powershell
cd backend
.\deploy.ps1
```

**Linux/Mac 用戶：**

```bash
cd backend
chmod +x build.sh
./build.sh
```

**手動 Docker 部署：**

```bash
cd backend
docker-compose up -d
```

部署後訪問：

- API 端點: <http://localhost:8000>
- API 文檔: <http://localhost:8000/docs>
- 健康檢查: <http://localhost:8000/api/healthy>

詳細部署指南請參閱 [`backend/README.md`](backend/README.md)

### 方式 3: 完整系統 Docker Compose

同時啟動前後端服務：

1. **確保已安裝 Docker 和 Docker Compose**

2. **設置環境變數**（在 `backend/` 目錄建立 `.env`）

   ```env
   GOOGLE_API_KEY=your_api_key_here
   ```

3. **啟動所有服務**

   ```bash
   docker-compose up --build
   ```

4. **訪問應用**
   - 前端: <http://localhost> (port 80)
   - 後端 API: <http://localhost:8000>
   - API 文檔: <http://localhost:8000/docs>

### 方式 4: 本地開發模式

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

## ✅ 劍魔吐槽系統實現

完整的吐槽邏輯已實現於 `backend/rag_core.py`，包含：

### 核心功能

- ✅ **劍魔語錄庫**: 7 條經典語錄，隨機抽取
- ✅ **諷刺風格 Prompt**: 用「找自己問題」的邏輯進行黑色幽默吐槽
- ✅ **多 LLM 支援**: 自動檢測並初始化可用的 LLM
- ✅ **自動降級機制**: LLM 初始化失敗時使用備用回應模式
- ✅ **社會議題延伸**: 把個人煩惱延伸到社會現象諷刺

### 回應風格

AI 會按照以下結構回應：
1. 先用「怎麼不找找自己的問題？」的邏輯諷刺一番
2. 把問題延伸到荒謬的社會現象
3. 最後給一個真正有意義的建議（用諷刺語氣包裝）

## 🆓 免費 LLM 支援

本專案支援多種免費 LLM 提供商：

| LLM | 費用 | 速度 | 額度 | 安裝 | 推薦度 |
|-----|------|------|------|------|--------|
| **Google Gemini 2.5 Flash** | 免費 | 快 | 1500次/日 | `pip install langchain-google-genai` | ⭐⭐⭐⭐⭐ |
| **Groq (Llama 3.1 70B)** | 免費 | 超快 | 30次/分 | `pip install langchain-groq` | ⭐⭐⭐⭐ |
| **Ollama** | 免費 | 中等 | 無限制 | 需安裝 Ollama | ⭐⭐⭐ |
| **OpenAI GPT-4** | 付費 | 快 | 依付費方案 | 內建 | ⭐⭐⭐⭐ |

**自動檢測順序**: Gemini → Groq → Ollama → OpenAI

系統會自動檢測可用的 LLM，優先使用 Gemini。如果所有 LLM 都不可用，將使用備用回應模式。

## 📚 資料與環境配置

### 1. 準備文本資料

在 `backend/books/` 或 `books/` 目錄放置文本文件（`.txt` 格式）：

**選項 A: 自動下載（推薦）**

```bash
# 使用快速設置腳本（會自動下載）
.\setup.ps1
```

**選項 B: 手動下載**

```powershell
# 下載聖嚴法師《真正的快樂》
Invoke-WebRequest -Uri "https://github.com/yenlung/AI-Demo/raw/refs/heads/master/books.zip" -OutFile "books.zip"
Expand-Archive -Path "books.zip" -DestinationPath "."
Remove-Item "books.zip"
```

**選項 C: 使用自己的文本**

將任意 `.txt` 文件放入 `backend/books/` 目錄即可。

### 2. 配置 LLM API Key

在 `backend/` 目錄下建立 `.env` 檔案：

**Google Gemini（推薦）：**

```env
GOOGLE_API_KEY=AIza...your_key_here
```

註冊網址：<https://aistudio.google.com/app/apikey>

**Groq（免費且快速）：**

```env
GROQ_API_KEY=gsk_...your_key_here
```

註冊網址：<https://console.groq.com/keys>

**Ollama（本地免費）：**

不需要 API Key，但需要：

1. 安裝 Ollama：<https://ollama.ai>
2. 下載模型：`ollama pull llama3.1`
3. 啟動服務：`ollama serve`

**OpenAI（付費）：**

```env
OPENAI_API_KEY=sk-...your_key_here
```

### 3. 安裝相應的套件

根據選擇的 LLM，安裝對應套件：

```bash
# Google Gemini
pip install langchain-google-genai

# Groq
pip install langchain-groq

# Ollama（通常已包含在 langchain-community）
pip install langchain-community

# OpenAI（已包含在 requirements.txt）
```

### 備用模式

即使沒有資料或 API Key，系統仍可運行，但會使用簡化的備用回應模式。

## 📡 API 端點

### GET `/api/healthy`

健康檢查端點，返回服務狀態與 RAG 系統初始化狀態。

**回應:**

```json
{
  "message": "Mind Healer API is running",
  "status": "healthy",
  "rag_initialized": true
}
```

### POST `/api/chat`

提交使用者問題並獲取劍魔吐槽。

**請求:**

```json
{
  "question": "我工作好累，老闆一直加班怎麼辦？"
}
```

**回應:**

```json
{
  "prescription": "怎麼不找找自己的問題？",
  "advice": "你說你工作累？怎麼不找找自己的問題？為什麼別人不用加班就你要加班？...(劍魔風格吐槽)"
}
```

**錯誤回應:**

```json
{
  "detail": "處理請求時發生錯誤: ..."
}
```

## 🛠️ 技術棧

### 後端

- **FastAPI** 0.109.0 - 現代、高效能的 Python Web 框架
- **LangChain** 0.1.20 - LLM 應用開發框架
- **LangChain Google GenAI** - Google Gemini 整合
- **LangChain Groq** - Groq LLM 整合
- **LangChain Community** - Ollama 等社群 LLM 支援
- **Pydantic** 2.5.3 - 資料驗證與序列化
- **Uvicorn** 0.27.0 - ASGI 伺服器
- **Python-dotenv** - 環境變數管理
- **NumPy** 1.26.3 - 數值計算（隨機抽取）

### 前端

- **Vue 3** 3.4.15 - 漸進式 JavaScript 框架
- **TypeScript** 5.3.3 - 型別安全的 JavaScript 超集
- **Vite** 5.0.11 - 快速的前端建置工具
- **Axios** 1.6.5 - HTTP 客戶端

### AI/ML

- **Google Gemini 2.5 Flash** - 主要 LLM（免費）
- **Groq Llama 3.1 70B** - 備用 LLM（免費）
- **Ollama** - 本地 LLM 支援
- **OpenAI GPT-4** - 付費 LLM 選項

### 部署

- **Docker** - 容器化技術
- **Docker Compose** - 多容器編排
- **Nginx** - 靜態文件伺服器與反向代理

## 📝 開發特性

### 已實現功能

✅ **完整的 RAG 系統**

- 文本直接載入（無需 embedding）
- 智慧內容檢索與回應生成
- 自動 LLM 檢測與 fallback

✅ **前端功能**

- 響應式設計（支援手機/平板/桌面）
- 即時載入狀態與錯誤處理
- 優雅的 UI/UX 設計
- CORS 完整配置

✅ **部署功能**

- Windows/Linux 自動部署腳本
- 健康檢查與日誌監控
- 環境變數配置管理
- 生產環境最佳化

### 開發建議

1. **CORS 已配置**: 支援本地開發與生產環境
2. **熱重載**: 前後端都支援開發時的熱重載
3. **錯誤處理**: 多層次錯誤處理與友善錯誤訊息
4. **環境隔離**: 開發/生產環境配置分離

## 🐛 除錯指南

### 檢查服務狀態

**後端健康檢查：**

```bash
curl http://localhost:8000/api/healthy
```

**查看容器狀態：**

```bash
docker ps
docker-compose ps
```

### 查看日誌

**查看所有日誌：**

```bash
docker-compose logs -f
```

**查看特定服務：**

```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 常見問題

**1. RAG 系統初始化失敗**

- 檢查 `.env` 文件是否正確配置
- 確認 API Key 格式正確
- 檢查 `books/` 目錄是否有文本文件

**2. 容器無法啟動**

```bash
# 重建映像
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

**3. 前端無法連接後端**

- 檢查後端是否正常運行：`curl http://localhost:8000/api/healthy`
- 檢查 Docker 網路：`docker network ls`
- 查看前端環境變數配置

### 重置專案

**停止並清除所有容器：**

```bash
docker-compose down -v
```

**重新建置並啟動：**

```bash
docker-compose up --build --force-recreate
```

## 📦 生產環境部署

### 部署檢查清單

- [ ] 配置生產環境 API Key
- [ ] 設定 HTTPS（建議使用 Let's Encrypt）
- [ ] 配置防火牆規則
- [ ] 設定 Nginx 反向代理（如需）
- [ ] 配置日誌輪轉
- [ ] 設定自動重啟策略
- [ ] 備份 `.env` 文件（但不要提交到版本控制）

### Docker 生產部署

1. **修改 `docker-compose.yaml`**（移除開發用 volume）
2. **設置環境變數**（使用生產用 API Key）
3. **背景啟動服務**

   ```bash
   docker-compose up -d
   ```

4. **配置 HTTPS**（使用 Certbot + Nginx）

### 監控與維護

**查看資源使用：**

```bash
docker stats
```

**更新部署：**

```bash
git pull
docker-compose down
docker-compose up -d --build
```

## 🔒 安全注意事項

- ⚠️ **不要**將 `.env` 文件提交到版本控制
- ⚠️ **不要**在公開場所暴露 API Key
- ✅ 生產環境使用環境變數而非 `.env` 文件
- ✅ 配置 HTTPS 和 SSL 證書
- ✅ 定期更新依賴套件
- ✅ 限制 API 請求速率（如需）

## 📄 授權

MIT License - 自由使用、修改與分發

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

### 貢獻指南

1. Fork 專案
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## � 更新日誌

### 最新版本

**✨ 功能完整版**

- ✅ 完整實現 RAG 系統（`rag_core.py`）
- ✅ 多 LLM 支援（Gemini/Groq/Ollama/OpenAI）
- ✅ 自動 LLM 檢測與降級機制
- ✅ 前後端獨立 Docker 部署腳本
- ✅ 健康檢查 API 端點
- ✅ 環境變數配置管理
- ✅ 快速設置腳本（`setup.ps1`）
- ✅ 完整的錯誤處理與日誌
- ✅ 生產環境配置優化
- ✅ 響應式前端設計
- ✅ API 文檔（Swagger）

### 技術改進

1. **RAG 系統**：實現文本直接載入策略，避免 embedding 配額限制
2. **部署優化**：提供 Windows/Linux 跨平台部署腳本
3. **容錯設計**：多層次降級機制，確保服務穩定性
4. **監控功能**：健康檢查與 RAG 初始化狀態監控
5. **開發體驗**：完整的文檔、設置腳本與錯誤處理

## 🎯 未來計劃

- [ ] 支援更多心靈書籍資料源
- [ ] 加入對話歷史記錄
- [ ] 實現使用者偏好設定
- [ ] 支援多語言（英文、簡體中文）
- [ ] 加入情緒分析功能
- [ ] 實現 RESTful API 版本控制
- [ ] 加入快取機制提升效能
- [ ] 支援 PostgreSQL 資料庫
- [ ] 實現使用者認證系統


## 🙏 致謝

- **yenlung** - 提供原始 RAG 心靈處方籤概念與實作
- **小明劍魔** - B站實況主，提供經典迷因語錄靈感
- Google Gemini 提供的免費 LLM 服務
- LangChain 社群的優秀框架
- FastAPI 與 Vue.js 社群
- 所有開源貢獻者

## 📞 聯絡資訊

- **專案名稱**: 小明劍魔 AI 吐槽系統
- **作者**: Daisy2100
- **Repository**: <https://github.com/Daisy2100/mind-healer>

## 📚 相關文件

- [`backend/README.md`](backend/README.md) - 後端部署指南
- [`setup.ps1`](setup.ps1) - 快速設置腳本
- [`docker-compose.yaml`](docker-compose.yaml) - Docker Compose 配置

---

**Built with ⚔️ using Vue 3, FastAPI, LangChain and 七連敗的怒火**

*怎麼不找找自己的問題？*

*最後更新：2025-11-27*
