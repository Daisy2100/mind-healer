# Mind Healer 專案檢查清單

使用此清單確保所有設置都已正確完成。

## 📋 安裝前檢查

### 必要軟體
- [ ] Python 3.11+ 已安裝
  ```powershell
  python --version
  ```
- [ ] Node.js 18+ 已安裝（如果本地開發前端）
  ```powershell
  node --version
  ```
- [ ] Docker Desktop 已安裝（如果使用 Docker）
  ```powershell
  docker --version
  docker-compose --version
  ```

### 帳號準備
- [ ] 有 OpenAI API Key
- [ ] OpenAI 帳戶有足夠額度

## 🗂️ 檔案結構檢查

### 必要檔案
- [ ] `backend/main.py` 存在
- [ ] `backend/rag_core.py` 存在
- [ ] `backend/requirements.txt` 存在
- [ ] `backend/Dockerfile` 存在
- [ ] `frontend/src/App.vue` 存在
- [ ] `frontend/package.json` 存在
- [ ] `frontend/Dockerfile` 存在
- [ ] `docker-compose.yaml` 存在

### 資料檔案
- [ ] `books/` 資料夾存在
- [ ] `books/` 內有至少一個 `.txt` 檔案
  ```powershell
  Get-ChildItem books\*.txt
  ```

### 環境設定
- [ ] `backend/.env` 檔案已建立
- [ ] `backend/.env` 包含 `OPENAI_API_KEY=sk-...`
- [ ] API Key 格式正確（以 `sk-` 開頭）

## 🔧 功能檢查

### 後端檢查

#### 1. 依賴安裝
```powershell
cd backend
pip install -r requirements.txt
```
- [ ] 所有套件安裝成功
- [ ] 沒有版本衝突錯誤

#### 2. 後端啟動
```powershell
python main.py
```
- [ ] 顯示「Mind Healer API 正在啟動...」
- [ ] 顯示「RAG 系統初始化完成」
- [ ] 沒有錯誤訊息
- [ ] 伺服器運行在 `http://0.0.0.0:8000`

#### 3. API 測試
訪問 `http://localhost:8000/`
- [ ] 返回 JSON 格式回應
- [ ] `status` 為 `"healthy"`
- [ ] `rag_initialized` 為 `true`

訪問 `http://localhost:8000/docs`
- [ ] 顯示 Swagger UI 文檔
- [ ] 可以看到 `/api/chat` 端點

#### 4. RAG 功能測試
使用 API 文檔或 curl 測試：
```powershell
$body = @{question = "測試問題"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api/chat" -Method Post -Body $body -ContentType "application/json"
```
- [ ] 返回包含 `prescription` 和 `advice` 的 JSON
- [ ] `prescription` 是心靈處方籤文字
- [ ] `advice` 是 AI 生成的建議
- [ ] 沒有錯誤訊息

### 前端檢查

#### 1. 依賴安裝
```powershell
cd frontend
npm install
```
- [ ] 所有套件安裝成功
- [ ] 沒有嚴重錯誤（警告可以忽略）

#### 2. 前端啟動
```powershell
npm run dev
```
- [ ] Vite 伺服器啟動成功
- [ ] 顯示本地地址（如 `http://localhost:5173`）
- [ ] 沒有編譯錯誤

#### 3. UI 測試
訪問 `http://localhost:5173`
- [ ] 頁面正常載入
- [ ] 看到「🧘‍♀️ 心靈處方籤」標題
- [ ] 有文字輸入框
- [ ] 有「🙏 求籤」按鈕
- [ ] 樣式正常顯示（漸層背景、卡片等）

#### 4. 功能測試
在前端介面中：
- [ ] 輸入問題後點擊「求籤」
- [ ] 顯示載入狀態（按鈕變為「求籤中...」）
- [ ] 成功顯示籤詩
- [ ] 成功顯示 AI 建議
- [ ] 可以點擊「重置」清空內容

### Docker 檢查

#### 1. 建置測試
```powershell
docker-compose build
```
- [ ] 後端映像建置成功
- [ ] 前端映像建置成功
- [ ] 沒有建置錯誤

#### 2. 啟動測試
```powershell
docker-compose up
```
- [ ] 兩個容器都成功啟動
- [ ] 後端日誌顯示「RAG 系統初始化完成」
- [ ] 前端日誌顯示 Nginx 已啟動
- [ ] 沒有連接錯誤

#### 3. 容器狀態
```powershell
docker-compose ps
```
- [ ] `mind-healer-backend` 狀態為 `Up`
- [ ] `mind-healer-frontend` 狀態為 `Up`

#### 4. 網路測試
訪問 `http://localhost/`
- [ ] 前端頁面正常載入
- [ ] 可以成功呼叫後端 API
- [ ] 功能完整正常

## 🎯 端對端測試

### 完整流程測試
1. [ ] 啟動完整系統（Docker 或本地）
2. [ ] 訪問前端介面
3. [ ] 輸入測試問題：「我最近工作壓力很大，該如何面對？」
4. [ ] 點擊求籤按鈕
5. [ ] 等待回應（約 5-10 秒）
6. [ ] 檢查籤詩是否為五條之一：
   - 感謝給我們機會，順境、逆境，皆是恩人。
   - 身心常放鬆，逢人面帶笑...
   - 識人識己識進退...
   - 平常心就是最自在、最愉快的心。
   - 知道自己的缺點愈多...
7. [ ] 檢查 AI 建議是否合理且相關
8. [ ] 測試「重置」按鈕
9. [ ] 嘗試輸入不同問題
10. [ ] 確認每次返回的籤詩可能不同（隨機）

## 📊 效能檢查

### 回應時間
- [ ] API 回應時間 < 15 秒（取決於網路和 OpenAI）
- [ ] 前端頁面載入 < 2 秒
- [ ] UI 操作流暢無延遲

### 資源使用
- [ ] 後端記憶體使用 < 1GB
- [ ] 前端記憶體使用 < 500MB
- [ ] CPU 使用合理

## 🔒 安全檢查

- [ ] `.env` 檔案在 `.gitignore` 中
- [ ] API Key 沒有被提交到 Git
- [ ] CORS 設定正確（只允許必要的來源）
- [ ] 敏感資訊沒有暴露在前端

## 📝 文檔檢查

- [ ] README.md 完整且易懂
- [ ] QUICKSTART.md 存在
- [ ] DATA_SETUP.md 存在
- [ ] 所有範例指令都可執行

## 🐛 錯誤處理檢查

### 後端錯誤處理
- [ ] 無效的請求返回適當錯誤訊息
- [ ] OpenAI API 失敗時有錯誤處理
- [ ] 資料庫檢索失敗時有備用方案

### 前端錯誤處理
- [ ] API 失敗時顯示錯誤訊息
- [ ] 空輸入時有提示
- [ ] 網路錯誤時有友善提示

## ✅ 最終確認

### 生產準備度
- [ ] 所有功能正常運作
- [ ] 沒有明顯的 bug
- [ ] 效能可接受
- [ ] 錯誤處理完善
- [ ] 文檔完整

### 部署準備
- [ ] Docker 映像建置成功
- [ ] 環境變數配置正確
- [ ] 依賴版本明確
- [ ] 有備份和恢復計畫

## 📈 下一步

完成所有檢查後：

1. **本地開發**
   - [ ] 開始修改和客製化
   - [ ] 添加更多心靈處方籤
   - [ ] 調整 UI 設計

2. **資料準備**
   - [ ] 添加更多書籍資料
   - [ ] 優化文本分割參數
   - [ ] 測試不同資料源

3. **功能擴展**
   - [ ] 添加使用者歷史記錄
   - [ ] 實作收藏功能
   - [ ] 添加分享功能

4. **部署計畫**
   - [ ] 選擇雲端平台
   - [ ] 配置 CI/CD
   - [ ] 設定監控和日誌

---

## 🆘 遇到問題？

如果任何項目無法勾選，請參考：

1. **QUICKSTART.md** - 快速啟動指南
2. **DATA_SETUP.md** - 資料準備詳細說明
3. **README.md** - 完整專案文檔
4. 檢查控制台/終端的錯誤訊息
5. 查看 Docker 日誌：`docker-compose logs`

常見問題通常是：
- API Key 未設置或錯誤
- books 資料夾缺失
- 埠號被占用
- 依賴套件版本衝突

---

**提示**: 將此檔案列印出來，在設置過程中逐項勾選，確保不遺漏任何步驟！
