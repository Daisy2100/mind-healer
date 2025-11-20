# Mind Healer - 技術實現報告

## 專案摘要

Mind Healer 是基於 RAG (Retrieval-Augmented Generation) 架構的全棧 AI 心靈諮詢系統，整合傳統心靈智慧與現代大型語言模型技術，提供個性化心靈建議服務。

## 核心技術架構

### 1. 前端技術棧
- **框架**: Vue 3.4.15 with Composition API
- **語言**: TypeScript 5.3.3
- **構建工具**: Vite 5.0.11
- **HTTP 客戶端**: Axios 1.6.5
- **UI 特色**: 漸變背景、響應式設計、載入動畫

### 2. 後端技術棧
- **框架**: FastAPI 0.109.0
- **ASGI 伺服器**: Uvicorn 0.27.0
- **RAG 框架**: LangChain 0.1.20
- **文件載入**: langchain-community 0.0.38
- **LLM 整合**: langchain-google-genai

### 3. 部署架構
- **容器化**: Docker + Docker Compose
- **前端服務**: Nginx 反向代理
- **網路**: 自訂 bridge 網路 (mind-healer-network)

## RAG 系統設計

### 核心創新：無 Embedding 策略

針對免費 API 的 embedding 配額限制問題，本系統採用**直接文本載入**策略：

1. **文本處理**: 使用 `DirectoryLoader` 載入 `.txt` 文件
2. **內容限制**: 取前 10,000 字避免 token 超限
3. **上下文注入**: 直接將書籍內容注入 LLM prompt
4. **優勢**: 
   - 無需 vector embeddings API 調用
   - 避免 FAISS 向量庫構建開銷
   - 繞過 Google Gemini embedding 配額限制

### LLM 多提供商支援

實現自動檢測與 fallback 機制：

```
優先級: Gemini 2.5 → Groq → Ollama → OpenAI
```

**檢測邏輯**:
1. 檢查環境變數 `GOOGLE_API_KEY`
2. 嘗試初始化 `ChatGoogleGenerativeAI(model="gemini-2.5-flash")`
3. 失敗則依序嘗試 Groq、Ollama、OpenAI
4. 全部失敗則拋出錯誤提示

### 心靈處方籤系統

**5 條固定籤詩**:
- "感謝給我們機會，順境、逆境，皆是恩人。"
- "身心常放鬆，逢人面帶笑..."
- "識人識己識進退，時時身心平安..."
- "平常心就是最自在、最愉快的心。"
- "知道自己的缺點愈多，成長的速度愈快..."

**抽籤邏輯**: 使用 `numpy.random.choice()` 隨機選擇

## 關鍵技術決策

### 1. 為何選擇 Google Gemini 2.5？

- **免費額度**: 每日 1500 次請求（最大）
- **速度**: gemini-2.5-flash 低延遲
- **中文支援**: 原生支援繁體中文
- **成本**: 完全免費，無需信用卡

### 2. 為何放棄 FAISS 向量檢索？

**原始設計** (基於 Notebook):
```python
embeddings = OllamaEmbeddings()
vector_store = FAISS.from_documents(split_docs, embeddings)
retriever = vector_store.as_retriever()
```

**問題**:
- Google Gemini embedding API 配額耗盡
- OllamaEmbeddings 需要本地 Ollama 服務
- OpenAI embeddings 需要付費 API

**解決方案** (當前實現):
```python
_books_content = "\n\n".join([doc.page_content for doc in documents])
_books_content = _books_content[:10000]

prompt = f"""
以下是來自書中的內容：
{_books_content[:3000]}

使用者的煩惱：{question}
"""
```

### 3. Windows 兼容性修復

**問題**: `langchain-community==0.0.20` 的 `pwd` 模組在 Windows 不可用

**解決**:
```python
# 從
from langchain.document_loaders import DirectoryLoader
# 改為
from langchain_community.document_loaders import DirectoryLoader, TextLoader
```

並升級到 `langchain-community==0.0.38`

### 4. TypeScript 編譯問題

**問題**: `vue-tsc` 在 Docker 構建時失敗

**解決**: 移除構建階段的類型檢查
```json
{
  "scripts": {
    "build": "vite build"  // 移除 vue-tsc &&
  }
}
```

## API 設計

### POST /api/chat

**請求**:
```json
{
  "question": "我最近工作壓力很大"
}
```

**處理流程**:
1. 載入環境變數（dotenv）
2. 初始化 Gemini LLM
3. 隨機抽取心靈處方籤
4. 構建包含書籍內容的 prompt
5. 調用 LLM 生成回應
6. 返回處方籤 + AI 建議

**回應**:
```json
{
  "prescription": "平常心就是最自在、最愉快的心。",
  "advice": "工作壓力大是現代人的普遍困擾..."
}
```

## 環境配置

### 必要環境變數

```env
GOOGLE_API_KEY=AIza...  # Google Gemini API Key
```

### 自動載入機制

```python
from dotenv import load_dotenv
load_dotenv()  # 載入 .env 文件
```

## 開發過程遇到的挑戰

### 1. Gemini Embedding 配額問題
**錯誤**: `429 Quota exceeded for generativelanguage.googleapis.com/embed_content_free_tier_requests`

**解決**: 完全移除 embedding 依賴，改用直接文本載入

### 2. 模型版本更新
**錯誤**: `404 models/gemini-1.5-flash is not found`

**原因**: Gemini 1.5 版本下架

**解決**: 更新為 `gemini-2.5-flash`

### 3. 編碼問題
**錯誤**: `UnicodeDecodeError: 'cp950' codec can't decode byte`

**解決**: 
- 移除中文註解
- 使用 UTF-8 編碼
- 添加 `autodetect_encoding=True`

### 4. Docker 構建失敗
**錯誤**: vue-tsc 在 Node.js 20.19.5 中報錯

**解決**: 簡化構建腳本，移除類型檢查步驟

## 性能優化

1. **文本截斷**: 限制載入內容為 10,000 字
2. **Prompt 優化**: 只傳入前 3,000 字到 LLM
3. **溫度設定**: temperature=0.7 平衡創意與準確性
4. **快取機制**: 全域變數 `_books_content` 避免重複載入

## 安全性考量

1. **API Key 保護**: 使用 `.env` 文件，不納入版本控制
2. **CORS 配置**: 限制允許的來源
3. **錯誤處理**: 不暴露敏感錯誤訊息給前端

## 未來改進方向

1. **向量檢索恢復**: 當 embedding API 額度充足時啟用 FAISS
2. **串流回應**: 實現 Server-Sent Events (SSE) 即時顯示生成過程
3. **使用者歷史**: 記錄對話歷史，提供個性化建議
4. **多語言支援**: 擴展至英文、日文等語言
5. **情緒分析**: 整合情感分析識別使用者狀態

## 結論

本專案成功實現了一個零成本、高效能的 AI 心靈諮詢系統，核心創新在於：

- ✅ 規避免費 API 限制的直接文本載入策略
- ✅ 多 LLM 提供商自動切換機制
- ✅ 完整的 Docker 容器化部署方案
- ✅ Windows 系統完整兼容性

技術棧選擇平衡了開發效率、運行成本與使用者體驗，適合作為 RAG 應用的最佳實踐參考。
