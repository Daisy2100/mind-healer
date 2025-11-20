# Mind Healer 快速啟動指南

## 🚀 三步驟啟動

### 步驟 1: 下載資料
```powershell
# 下載書籍資料
Invoke-WebRequest -Uri "https://github.com/yenlung/AI-Demo/raw/refs/heads/master/books.zip" -OutFile "books.zip"

# 解壓縮
Expand-Archive -Path "books.zip" -DestinationPath "." -Force

# 刪除壓縮檔
Remove-Item "books.zip"
```

### 步驟 2: 設定 API Key
```powershell
# 複製範例檔案
Copy-Item "backend\.env.example" -Destination "backend\.env"

# 編輯 .env 檔案，填入你的 OpenAI API Key
notepad backend\.env
```

在 `.env` 中填入：
```
OPENAI_API_KEY=sk-your-api-key-here
```

### 步驟 3: 啟動專案

#### 選項 A: 使用 Docker（推薦）
```powershell
docker-compose up --build
```

#### 選項 B: 本地開發

**後端：**
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

**前端（新終端）：**
```powershell
cd frontend
npm install
npm run dev
```

## 📍 訪問應用

- 🌐 前端介面: http://localhost (Docker) 或 http://localhost:5173 (本地)
- 🔌 後端 API: http://localhost:8000
- 📚 API 文檔: http://localhost:8000/docs

## ✅ 驗證安裝

訪問 http://localhost:8000/ 應該看到：
```json
{
  "message": "Mind Healer API is running",
  "status": "healthy",
  "rag_initialized": true
}
```

如果 `rag_initialized` 是 `false`，請檢查：
1. `books/` 資料夾是否存在
2. `books/` 中是否有 `.txt` 檔案
3. `OPENAI_API_KEY` 是否正確設定

## 🎯 使用應用

1. 打開前端介面
2. 在文字框中輸入你的煩惱或問題
3. 點擊「🙏 求籤」按鈕
4. 系統會：
   - 隨機抽取一支心靈處方籤
   - 使用 RAG 從書籍資料庫檢索相關內容
   - 結合 GPT-4 生成個性化建議

## 🔧 常用命令

### Docker 相關
```powershell
# 啟動
docker-compose up

# 背景啟動
docker-compose up -d

# 停止
docker-compose down

# 重新建置
docker-compose up --build --force-recreate

# 查看日誌
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 本地開發
```powershell
# 後端熱重載（使用 uvicorn）
cd backend
uvicorn main:app --reload

# 前端熱重載（自動）
cd frontend
npm run dev

# 安裝新的 Python 套件
cd backend
pip install package-name
pip freeze > requirements.txt

# 安裝新的 npm 套件
cd frontend
npm install package-name
```

## 📝 測試 API

### 使用 PowerShell
```powershell
$body = @{
    question = "我最近工作壓力很大，該如何面對？"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/chat" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"
```

### 使用 curl（Git Bash 或 WSL）
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "我最近工作壓力很大"}'
```

## 🐛 疑難排解

### 問題 1: Docker 建置失敗
```powershell
# 清理 Docker 快取
docker system prune -a

# 重新建置
docker-compose build --no-cache
docker-compose up
```

### 問題 2: 埠號被占用
如果 8000 或 5173 埠被占用，可以修改 `docker-compose.yaml` 或 `vite.config.ts`

### 問題 3: NLTK 資料缺失
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -c "import nltk; nltk.download('punkt')"
```

### 問題 4: OpenAI API 錯誤
確認：
- API Key 正確無誤
- 帳戶有足夠的額度
- 網路連接正常

## 📦 專案結構
```
mind-healer/
├── backend/              # FastAPI 後端
│   ├── main.py          # API 入口
│   ├── rag_core.py      # RAG 核心邏輯
│   ├── requirements.txt # Python 依賴
│   └── .env            # 環境變數（需自行建立）
├── frontend/            # Vue 3 前端
│   ├── src/
│   │   └── App.vue     # 主介面
│   ├── package.json
│   └── vite.config.ts
├── books/              # 書籍資料（需自行下載）
│   └── *.txt
├── docker-compose.yaml # Docker 編排
└── README.md           # 專案說明
```

## 🎓 進階設定

### 自訂心靈處方籤
編輯 `backend/rag_core.py` 中的 `SPIRITUAL_PRESCRIPTIONS` 列表

### 更換 LLM 模型
在 `backend/rag_core.py` 中修改：
```python
_llm = ChatOpenAI(model="gpt-3.5-turbo")  # 改用 GPT-3.5
```

### 調整檢索參數
在 `initialize_rag_system` 函式中修改：
```python
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}  # 檢索更多相關文檔
)
```

### 修改 UI 樣式
編輯 `frontend/src/App.vue` 中的 `<style>` 區塊

## 📚 更多資訊

- 詳細資料準備說明: [DATA_SETUP.md](DATA_SETUP.md)
- 完整專案說明: [README.md](README.md)

---

✨ 祝你使用愉快！如有問題歡迎查閱文檔或提出 Issue。
