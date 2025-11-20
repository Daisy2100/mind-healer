# 🆓 使用免費 LLM 的指南

如果你沒有 OpenAI API Key 或預算有限，這裡提供幾個免費/低成本的替代方案！

## 🌟 推薦方案 1：Google Gemini (免費額度最大)

### 什麼是 Gemini？
- **完全免費**的 API 服務（額度最大）
- Google 最新的 AI 模型
- **超大免費額度**：每天 1500 次請求
- 支援繁體中文，理解力優秀
- Gemini 1.5 Flash 速度快且免費

### 如何使用 Gemini

#### 1. 註冊並取得 API Key
1. 訪問 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 使用 Google 帳號登入（完全免費）
3. 點擊 "Create API Key"
4. 複製 API Key（格式：`AIza...`）

#### 2. 安裝必要套件
```powershell
cd backend
pip install langchain-google-genai
```

#### 3. 設定環境變數
在 `backend/.env` 中添加：
```env
GOOGLE_API_KEY=AIza_your_api_key_here
```

#### 4. 啟動專案
```powershell
# Docker
docker-compose up --build

# 或本地
cd backend
python main.py
```

### Gemini 可用模型
- `gemini-1.5-flash` - 快速且免費（推薦）
- `gemini-1.5-pro` - 功能更強大
- `gemini-pro` - 穩定版本

### 使用限制（免費版）
- 每分鐘：15 次請求
- 每天：1500 次請求
- 每月：無限制（只要不超過每日額度）
- **對個人專案非常夠用！**

---

## 🌟 推薦方案 2：Groq (免費 + 超快)

### 什麼是 Groq？
- **完全免費**的 API 服務（有額度限制）
- **超快速度**（比 OpenAI 快 10-20 倍）
- 提供 Llama 3.1 70B、Mixtral 等強大模型
- 每分鐘 30 次請求的免費額度

### 如何使用 Groq

#### 1. 註冊並取得 API Key
1. 訪問 [Groq Console](https://console.groq.com/keys)
2. 使用 Google 或 Email 註冊（完全免費）
3. 建立新的 API Key
4. 複製 API Key（格式：`gsk_...`）

#### 2. 安裝必要套件
```powershell
cd backend
pip install langchain-groq
```

#### 3. 設定環境變數
在 `backend/.env` 中添加：
```env
GROQ_API_KEY=gsk_your_api_key_here
```

#### 4. 啟動專案
```powershell
# Docker
docker-compose up --build

# 或本地
cd backend
python main.py
```

### Groq 可用模型
- `llama-3.1-70b-versatile` - 最強大（推薦）
- `llama-3.1-8b-instant` - 最快速
- `mixtral-8x7b-32768` - 長文本處理

### 使用限制
- 免費額度：每分鐘 30 次請求
- 每天約 14,400 次請求
- 對於個人專案完全足夠！

---

## 🏠 方案 2：Ollama (完全免費，本地運行)

### 什麼是 Ollama？
- **完全免費**且開源
- 在你的電腦上**本地運行**
- 不需要網路連接
- 不需要 API Key
- 隱私完全保護

### 如何使用 Ollama

#### 1. 安裝 Ollama
- Windows: 下載 [Ollama for Windows](https://ollama.ai/download/windows)
- Mac: `brew install ollama`
- Linux: `curl https://ollama.ai/install.sh | sh`

#### 2. 下載模型
```powershell
# 下載 Llama 3.1 (推薦)
ollama pull llama3.1

# 或其他模型
ollama pull mistral
ollama pull llama2
```

#### 3. 啟動 Ollama 服務
```powershell
ollama serve
```

#### 4. 啟動 Mind Healer
不需要設定 API Key，直接啟動即可：
```powershell
cd backend
python main.py
```

### 系統需求
- **記憶體**: 至少 8GB RAM（推薦 16GB）
- **硬碟**: 4-8GB（每個模型）
- **處理器**: 現代 CPU（有 GPU 更好）

### 可用模型
- `llama3.1` - Meta 最新模型（推薦）
- `mistral` - 快速且高效
- `llama2` - 穩定的選擇
- `codellama` - 程式碼專用

---

## 💰 方案 3：OpenAI (付費，效果最好)

如果你需要最好的品質，OpenAI 仍是首選：

### 價格（2024）
- **GPT-4o**: $5 / 1M tokens (輸入)
- **GPT-3.5-turbo**: $0.5 / 1M tokens
- 新用戶通常有 $5 免費額度

### 設定方式
```env
OPENAI_API_KEY=sk_your_openai_api_key_here
```

---

## 🔄 自動選擇邏輯

我們的系統會自動按照優先順序選擇可用的 LLM：

1. **Groq** - 如果有 `GROQ_API_KEY`
2. **Ollama** - 如果本地有 Ollama 服務
3. **OpenAI** - 如果有 `OPENAI_API_KEY`

只要設定其中一個，系統就能運行！

---

## 📊 各方案比較

| 特性 | Gemini | Groq | Ollama | OpenAI |
|------|--------|------|--------|--------|
| **價格** | 免費 | 免費 | 免費 | 付費 |
| **免費額度** | 1500/天 | 30/分鐘 | 無限 | 無 |
| **速度** | ⚡⚡ 快 | ⚡⚡⚡ 超快 | ⚡ 中等 | ⚡⚡ 快 |
| **品質** | 🌟🌟🌟🌟 優秀 | 🌟🌟🌟🌟 優秀 | 🌟🌟🌟 良好 | 🌟🌟🌟🌟🌟 最佳 |
| **中文支援** | ✅ 原生支援 | ✅ 良好 | ✅ 良好 | ✅ 最佳 |
| **隱私** | 雲端 | 雲端 | 🔒 完全本地 | 雲端 |
| **需要網路** | ✅ 是 | ✅ 是 | ❌ 否 | ✅ 是 |
| **安裝複雜度** | 簡單 | 簡單 | 中等 | 簡單 |
| **記憶體需求** | 無 | 無 | 8-16GB | 無 |

---

## 🎯 推薦方案

### 如果你...

**想要最大免費額度**: 選 **Gemini** ⭐
- ✅ 每天 1500 次請求
- ✅ Google 出品，品質保證
- ✅ 完美支援繁體中文
- ✅ 註冊簡單快速

**想要最快速度**: 選 **Groq**
- ✅ 免費且超快
- ✅ 只需註冊拿 API Key
- ✅ 不需要強大硬體

**注重隱私/離線使用**: 選 **Ollama**
- ✅ 資料不離開你的電腦
- ✅ 不需要網路
- ✅ 完全控制

**需要最佳品質**: 選 **OpenAI**
- ✅ 回應品質最高
- ✅ 最穩定
- ⚠️ 需要付費

---

## 🚀 快速開始 (Gemini - 推薦)

### 完整步驟（3 分鐘）

1. **註冊 Google Gemini**
   ```
   https://aistudio.google.com/app/apikey
   ```

2. **取得 API Key**
   - 使用 Google 帳號登入
   - 點擊 "Create API Key"
   - 複製 Key (AIza...)

3. **設定專案**
   ```powershell
   cd f:\develop\mind-healer
   .\setup.ps1
   # 選擇 "1. Google Gemini"
   # 貼上你的 API Key
   ```

4. **安裝套件**
   ```powershell
   cd backend
   pip install langchain-google-genai
   ```

5. **啟動！**
   ```powershell
   cd ..
   docker-compose up --build
   ```

---

## 💡 常見問題

### Q: Gemini 的免費額度夠用嗎？
**A**: 非常夠！每天 1500 次請求，是所有免費方案中最大的。即使重度使用也很難用完。

### Q: Groq 的免費額度夠用嗎？
**A**: 非常夠！每分鐘 30 次請求，對於個人專案綽綽有餘。

### Q: Ollama 會很慢嗎？
**A**: 取決於你的硬體。如果有 16GB RAM，速度還不錯。

### Q: 可以混用嗎？
**A**: 可以！設定多個 API Key，系統會自動選擇可用的。

### Q: 如何切換模型？
**A**: 編輯 `backend/rag_core.py`，修改模型名稱：
```python
# Gemini
_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Groq
_llm = ChatGroq(model="llama-3.1-70b-versatile")

# Ollama
_llm = Ollama(model="llama3.1")
```

### Q: Gemini 支援中文嗎？
**A**: 完美支援！Gemini 對繁體中文的理解非常好，是 Google 原生支援的語言。

### Q: Groq 支援中文嗎？
**A**: 完美支援！Llama 3.1 對中文的理解很好。

---

## 🆘 遇到問題？

### Gemini 錯誤: "Quota exceeded"
- 等待到隔天（每日額度重置）
- 或暫時使用 Groq/Ollama 作為備用

### Groq 錯誤: "Rate limit exceeded"
- 等待一分鐘再試
- 或使用 Gemini/Ollama 作為備用

### Ollama 連接失敗
- 確認 Ollama 服務正在運行：`ollama serve`
- 確認模型已下載：`ollama list`

### 都不可用
- 檢查網路連接（Groq/OpenAI）
- 檢查 API Key 格式
- 查看錯誤日誌：`docker-compose logs backend`

---

## 🎉 開始使用吧！

**推薦流程**：
1. 先試 **Gemini**（免費額度最大，Google 品質保證）⭐
2. 需要速度，試 **Groq**（免費且超快）
3. 需要離線，試 **Ollama**（本地免費）
4. 需要最佳品質時考慮 **OpenAI**

**記住**：你不需要 OpenAI 也能使用這個專案！Gemini、Groq 和 Ollama 都是很棒的免費選擇！🚀

### 🏆 最佳選擇建議

- **日常使用**: Gemini（額度最大，不用擔心用完）
- **快速測試**: Groq（速度最快）
- **長期開發**: Ollama（本地運行，完全免費）
- **生產環境**: OpenAI（品質最穩定）
