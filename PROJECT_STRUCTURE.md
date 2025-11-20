# 專案結構說明

```
mind-healer/
│
├── 📂 backend/                          # FastAPI 後端服務
│   ├── main.py                          # FastAPI 應用程式入口
│   ├── rag_core.py                      # RAG 核心邏輯（已整合 Notebook）
│   ├── requirements.txt                 # Python 依賴清單
│   ├── Dockerfile                       # 後端容器配置
│   ├── .env.example                     # 環境變數範例
│   └── .env                            # 環境變數（需自行建立）
│
├── 📂 frontend/                         # Vue 3 前端應用
│   ├── src/
│   │   ├── App.vue                     # 主應用元件（完整 UI）
│   │   ├── main.ts                     # 應用入口
│   │   ├── style.css                   # 全域樣式
│   │   └── vite-env.d.ts               # TypeScript 定義
│   ├── index.html                       # HTML 入口
│   ├── package.json                     # Node.js 依賴
│   ├── vite.config.ts                   # Vite 配置
│   ├── tsconfig.json                    # TypeScript 配置
│   ├── tsconfig.node.json               # Node TypeScript 配置
│   ├── Dockerfile                       # 前端容器配置
│   └── nginx.conf                       # Nginx 配置
│
├── 📂 books/                            # 資料目錄（需自行準備）
│   └── *.txt                           # 書籍文字檔案
│
├── 📄 docker-compose.yaml               # Docker 編排配置
├── 📄 .gitignore                        # Git 忽略規則
│
├── 📖 README.md                         # 專案主要說明文件
├── 📖 QUICKSTART.md                     # 快速啟動指南
├── 📖 DATA_SETUP.md                     # 資料準備詳細說明
├── 📖 CHECKLIST.md                      # 專案檢查清單
├── 📖 PROJECT_STRUCTURE.md              # 本檔案
│
├── 🔧 setup.ps1                         # 自動化設置腳本（Windows）
│
└── 📓 【Demo06】用_RAG_打造心靈處方籤機器人.ipynb  # 原始 Notebook

```

## 📁 目錄說明

### Backend（後端）

**`main.py`**
- FastAPI 應用程式入口
- 定義 API 路由和端點
- CORS 中介軟體配置
- 在啟動時初始化 RAG 系統
- 提供健康檢查端點

**`rag_core.py`**
- RAG 核心邏輯實作
- 從 Notebook 完整移植的功能：
  - FAISS 向量資料庫初始化
  - 文件載入和分割
  - 檢索增強生成（RAG）
  - 心靈處方籤隨機選取
  - GPT-4 回應生成
- 包含備用模式（無資料時）

**`requirements.txt`**
- FastAPI 和相關套件
- LangChain 及其依賴
- FAISS 向量資料庫
- OpenAI API 客戶端
- 其他必要套件

**`Dockerfile`**
- 基於 Python 3.11
- 安裝所有依賴
- 暴露 8000 埠
- 使用 Uvicorn 啟動

### Frontend（前端）

**`src/App.vue`**
- 主要 UI 元件
- 使用 Vue 3 Composition API (`<script setup>`)
- TypeScript 支援
- 包含：
  - 使用者輸入表單
  - 求籤按鈕和載入狀態
  - 籤詩顯示區
  - AI 建議顯示區
  - 錯誤處理
- 響應式設計（支援行動裝置）

**`package.json`**
- Vue 3 核心
- Axios HTTP 客戶端
- Vite 建置工具
- TypeScript 支援

**`vite.config.ts`**
- Vite 配置
- Vue 插件
- 開發伺服器設定
- API 代理配置

**`Dockerfile`**
- 多階段建置：
  - 階段 1: Node.js 建置
  - 階段 2: Nginx 提供服務
- 包含 Nginx 配置

### 配置檔案

**`docker-compose.yaml`**
- 編排前後端服務
- 配置網路和埠號映射
- Volume 掛載配置
- 環境變數設定

**`.gitignore`**
- 忽略 Python 快取和虛擬環境
- 忽略 Node.js modules
- 忽略環境變數檔案
- 忽略向量資料庫

### 文檔檔案

**`README.md`**
- 專案概述
- 完整的設置說明
- API 文檔
- 技術棧介紹
- 部署指南

**`QUICKSTART.md`**
- 三步驟快速啟動
- 常用命令參考
- 疑難排解
- 測試方法

**`DATA_SETUP.md`**
- 詳細的資料準備說明
- 多種資料來源選項
- 環境變數配置
- 驗證方法

**`CHECKLIST.md`**
- 完整的檢查清單
- 安裝前準備
- 功能測試項目
- 端對端測試
- 部署準備

### 工具腳本

**`setup.ps1`**
- Windows PowerShell 自動化腳本
- 自動下載資料
- 互動式設置 API Key
- 一鍵啟動選項

## 🔄 資料流

```
使用者 → 前端 (Vue 3)
         ↓
    API 請求 (/api/chat)
         ↓
    後端 (FastAPI)
         ↓
    RAG 核心 (rag_core.py)
         ↓
    ├─ 隨機抽取心靈處方籤
    │
    ├─ FAISS 檢索相關內容
    │  └─ 從 books/*.txt
    │
    ├─ 組合 Prompt
    │
    └─ 呼叫 OpenAI GPT-4
         ↓
    生成個性化建議
         ↓
    返回 JSON 回應
    {
      "prescription": "...",
      "advice": "..."
    }
         ↓
    前端顯示結果
```

## 🚀 啟動流程

### Docker 模式
1. `docker-compose build` - 建置映像
2. `docker-compose up` - 啟動容器
3. 後端初始化 RAG 系統
4. 前端由 Nginx 提供服務

### 本地開發模式

**後端：**
1. 建立虛擬環境
2. 安裝依賴 (`pip install -r requirements.txt`)
3. 設定環境變數 (`.env`)
4. 啟動 FastAPI (`python main.py`)
5. 初始化 RAG 系統

**前端：**
1. 安裝依賴 (`npm install`)
2. 啟動開發伺服器 (`npm run dev`)
3. Vite 提供熱重載

## 📦 核心依賴

### 後端
- **FastAPI**: Web 框架
- **LangChain**: RAG 框架
- **FAISS**: 向量資料庫
- **OpenAI**: LLM API
- **Uvicorn**: ASGI 伺服器

### 前端
- **Vue 3**: UI 框架
- **TypeScript**: 型別安全
- **Vite**: 建置工具
- **Axios**: HTTP 客戶端

## 🔐 環境變數

### 必須設定
- `OPENAI_API_KEY`: OpenAI API 金鑰

### 可選設定
- `BOOKS_DIR`: 自訂資料目錄路徑（預設：`books`）

## 📊 檔案大小估算

- 後端 Docker 映像: ~800MB
- 前端 Docker 映像: ~50MB
- books 資料: ~1-5MB（取決於內容）
- 向量資料庫（FAISS）: ~10-50MB（初始化後）

## 🛠️ 開發建議

### 修改後端邏輯
1. 編輯 `backend/rag_core.py`
2. 修改 `SPIRITUAL_PRESCRIPTIONS` 添加更多籤詩
3. 調整檢索參數（chunk_size, k 值等）
4. 更換 LLM 模型

### 修改前端 UI
1. 編輯 `frontend/src/App.vue`
2. 修改 `<style>` 區塊調整樣式
3. 更改 `<template>` 調整布局
4. 編輯 `<script>` 調整邏輯

### 添加新功能
1. 後端：在 `main.py` 添加新端點
2. 前端：在 `App.vue` 添加新元件
3. 更新文檔說明新功能

## 📚 相關資源

- [FastAPI 文檔](https://fastapi.tiangolo.com/)
- [Vue 3 文檔](https://vuejs.org/)
- [LangChain 文檔](https://python.langchain.com/)
- [FAISS 文檔](https://github.com/facebookresearch/faiss)
- [Docker 文檔](https://docs.docker.com/)

---

這個結構是為了：
- ✅ 清晰的關注點分離（前端/後端）
- ✅ 易於開發和測試
- ✅ 容器化部署準備
- ✅ 完整的文檔支援
- ✅ 便於維護和擴展
