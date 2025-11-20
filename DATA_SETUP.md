# 資料準備指南

## 📚 如何準備你的資料

你的 Notebook 使用了聖嚴法師的《真正的快樂》作為資料來源。要讓 RAG 系統正常運作，你需要準備文字資料。

### 方式 1: 使用 Notebook 中的資料（推薦）

如果你已經有 `books.zip` 檔案（從 Notebook 下載的），請按照以下步驟：

1. **解壓縮 books.zip**
   ```bash
   # 在專案根目錄下
   unzip books.zip
   ```

2. **確認資料結構**
   ```
   mind-healer/
   ├── backend/
   └── books/           # 資料夾應該在這裡
       └── *.txt        # 文字檔案
   ```

### 方式 2: 手動下載資料

如果你沒有 `books.zip`，可以在 Notebook 中執行以下命令來下載：

```python
# 在 Jupyter Notebook 中執行
!wget -O books.zip https://github.com/yenlung/AI-Demo/raw/refs/heads/master/books.zip
!unzip -o books.zip
```

然後將 `books/` 資料夾複製到專案根目錄。

### 方式 3: 使用你自己的資料

你可以使用任何 `.txt` 格式的文字資料：

1. **建立 books 資料夾**
   ```bash
   mkdir books
   ```

2. **放入你的文字檔案**
   - 支援任何 `.txt` 格式的檔案
   - 可以放入多個檔案
   - 內容應該是你希望 RAG 系統檢索的知識庫

3. **範例資料格式**
   ```
   books/
   ├── 真正的快樂.txt
   ├── 心靈雞湯.txt
   └── 其他書籍.txt
   ```

## 🔧 環境變數設定

### 必須設定

1. **OpenAI API Key**
   
   在 `backend/` 目錄下建立 `.env` 檔案：
   ```bash
   cd backend
   cp .env.example .env
   ```
   
   編輯 `.env` 並填入你的 API Key：
   ```env
   OPENAI_API_KEY=sk-your-api-key-here
   ```

### 可選設定

2. **自訂資料路徑**（如果你的資料不在 `books/` 資料夾）
   
   在 `.env` 中添加：
   ```env
   BOOKS_DIR=/path/to/your/books
   ```

## 🚀 啟動專案

### 確認資料已準備好

在啟動前，確認以下項目：

- [ ] `books/` 資料夾存在
- [ ] `books/` 資料夾內有 `.txt` 檔案
- [ ] `backend/.env` 已設定 `OPENAI_API_KEY`

### 啟動方式

#### 使用 Docker
```bash
# 在專案根目錄
docker-compose up --build
```

#### 本地開發
```bash
# 後端
cd backend
pip install -r requirements.txt
python main.py

# 前端（新終端）
cd frontend
npm install
npm run dev
```

## 📊 驗證 RAG 系統

1. **檢查後端啟動日誌**
   
   成功時會看到：
   ```
   ==================================================
   🧘‍♀️ Mind Healer API 正在啟動...
   ==================================================
   正在初始化 RAG 系統...
   ✓ RAG 系統初始化完成！載入了 X 個文件，分割為 Y 個片段。
   ```

2. **訪問健康檢查端點**
   
   開啟瀏覽器訪問：`http://localhost:8000/`
   
   應該看到：
   ```json
   {
     "message": "Mind Healer API is running",
     "status": "healthy",
     "rag_initialized": true
   }
   ```

3. **測試 API**
   
   使用前端介面或直接呼叫 API：
   ```bash
   curl -X POST http://localhost:8000/api/chat \
     -H "Content-Type: application/json" \
     -d '{"question": "我最近工作壓力很大"}'
   ```

## 🐛 常見問題

### 問題 1: `books/` 資料夾不存在
```
警告: 資料夾 'books' 不存在，將使用預設回應
```
**解決方法**: 按照上述「方式 1」或「方式 2」準備資料。

### 問題 2: OpenAI API Key 未設定
```
ValueError: 請設定 OPENAI_API_KEY 環境變數
```
**解決方法**: 建立 `backend/.env` 並設定 API Key。

### 問題 3: NLTK 資料缺失
```
LookupError: Resource punkt not found
```
**解決方法**: 在 Python 中執行：
```python
import nltk
nltk.download('punkt')
```

### 問題 4: 即使沒有資料也想測試

如果暫時沒有資料，系統會自動使用備用回應模式。你仍然可以：
- 啟動 API 和前端
- 測試介面功能
- 系統會返回基本的心靈處方籤（隨機選取）和簡單的建議

稍後準備好資料後，重新啟動服務即可啟用完整的 RAG 功能。

## 📝 版權聲明

如果你使用《法鼓全集》的資料，請注意：
- 版權屬「法鼓文化」所有
- 僅供學習和研究使用
- 商業用途請聯繫版權方

## 🔗 相關資源

- [法鼓全集](https://ddc.shengyen.org/)
- [原始 Notebook](https://github.com/yenlung/AI-Demo)
- [LangChain 文檔](https://python.langchain.com/)
- [FAISS 文檔](https://github.com/facebookresearch/faiss)
