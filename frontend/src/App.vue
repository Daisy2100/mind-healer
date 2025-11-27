<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

// In production, use empty string to use relative path (proxied by nginx)
// In development, use localhost
const API_BASE_URL = import.meta.env.VITE_API_URL !== undefined 
  ? import.meta.env.VITE_API_URL 
  : 'http://localhost:8000'

const userQuestion = ref('')
const prescription = ref('')
const advice = ref('')
const isLoading = ref(false)
const errorMessage = ref('')

const getPrescription = async () => {
  if (!userQuestion.value.trim()) {
    errorMessage.value = '怎麼不輸入你的問題？'
    return
  }

  isLoading.value = true
  errorMessage.value = ''
  prescription.value = ''
  advice.value = ''

  try {
    const response = await axios.post(`${API_BASE_URL}/api/chat`, {
      question: userQuestion.value
    })

    prescription.value = response.data.prescription
    advice.value = response.data.advice
  } catch (error: any) {
    errorMessage.value = error.response?.data?.detail || '系統炸了，但這不是你的問題！'
    console.error('Error:', error)
  } finally {
    isLoading.value = false
  }
}

const reset = () => {
  userQuestion.value = ''
  prescription.value = ''
  advice.value = ''
  errorMessage.value = ''
}
</script>

<template>
  <div class="app-container">
    <header class="header">
      <h1>⚔️ 小明劍魔 AI 吐槽系統</h1>
      <p class="subtitle">怎麼不找找自己的問題？</p>
      <p class="disclaimer">⚠️ 本系統為諷刺/迷因專案，僅供娛樂用途</p>
    </header>

    <main class="main-content">
      <div class="input-section">
        <label for="question">你的煩惱（讓劍魔來吐槽你）:</label>
        <textarea
          id="question"
          v-model="userQuestion"
          placeholder="說說你的煩惱...工作太累？買不起房？上不去分？全部來吧！"
          rows="5"
          :disabled="isLoading"
        ></textarea>

        <div class="button-group">
          <button 
            @click="getPrescription" 
            :disabled="isLoading"
            class="btn-primary"
          >
            {{ isLoading ? '劍魔思考中...(需要10秒左右)' : '⚔️ 讓劍魔吐槽我' }}
          </button>
          <button 
            @click="reset" 
            :disabled="isLoading"
            class="btn-secondary"
          >
            重開一局
          </button>
        </div>

        <div v-if="errorMessage" class="error-message">
          💢 {{ errorMessage }}
        </div>
      </div>

      <div v-if="prescription || advice" class="result-section">
        <div class="prescription-card">
          <h2>⚔️ 劍魔語錄</h2>
          <div class="prescription-text">
            {{ prescription }}
          </div>
        </div>

        <div class="advice-card">
          <h2>🗡️ 劍魔吐槽</h2>
          <div class="advice-text">
            {{ advice }}
          </div>
        </div>
      </div>
    </main>

    <footer class="footer">
      <p>Powered by 七連敗 & 黑色幽默 & RAG Technology</p>
      <p class="meme-credit">靈感來源：B站實況主小明劍魔</p>
    </footer>
  </div>
</template>

<style scoped>
* {
  box-sizing: border-box;
}

.app-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f0f23 100%);
  padding: 2rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.header {
  text-align: center;
  color: #ff4757;
  margin-bottom: 2rem;
}

.header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  text-shadow: 0 0 10px rgba(255, 71, 87, 0.5), 2px 2px 4px rgba(0, 0, 0, 0.5);
  animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
  from {
    text-shadow: 0 0 10px rgba(255, 71, 87, 0.5), 2px 2px 4px rgba(0, 0, 0, 0.5);
  }
  to {
    text-shadow: 0 0 20px rgba(255, 71, 87, 0.8), 0 0 30px rgba(255, 71, 87, 0.4), 2px 2px 4px rgba(0, 0, 0, 0.5);
  }
}

.subtitle {
  font-size: 1.3rem;
  color: #ffa502;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.disclaimer {
  font-size: 0.9rem;
  color: #747d8c;
  font-style: italic;
}

.main-content {
  max-width: 800px;
  margin: 0 auto;
}

.input-section {
  background: linear-gradient(145deg, #2d2d44, #1e1e2f);
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
  margin-bottom: 2rem;
  border: 1px solid rgba(255, 71, 87, 0.3);
}

label {
  display: block;
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #dfe4ea;
}

textarea {
  width: 100%;
  padding: 1rem;
  font-size: 1rem;
  border: 2px solid #3d3d5c;
  border-radius: 8px;
  resize: vertical;
  font-family: inherit;
  transition: border-color 0.3s, box-shadow 0.3s;
  background: #1a1a2e;
  color: #f1f2f6;
}

textarea::placeholder {
  color: #747d8c;
}

textarea:focus {
  outline: none;
  border-color: #ff4757;
  box-shadow: 0 0 10px rgba(255, 71, 87, 0.3);
}

textarea:disabled {
  background-color: #2d2d44;
  cursor: not-allowed;
  opacity: 0.7;
}

.button-group {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

button {
  flex: 1;
  padding: 1rem;
  font-size: 1.1rem;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background: linear-gradient(135deg, #ff4757 0%, #c0392b 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(255, 71, 87, 0.4);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 71, 87, 0.6);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: #3d3d5c;
  color: #dfe4ea;
  border: 1px solid #4a4a6a;
}

.btn-secondary:hover:not(:disabled) {
  background: #4a4a6a;
}

.error-message {
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(255, 71, 87, 0.1);
  color: #ff6b7a;
  border-radius: 8px;
  border-left: 4px solid #ff4757;
}

.result-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.prescription-card,
.advice-card {
  background: linear-gradient(145deg, #2d2d44, #1e1e2f);
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 71, 87, 0.2);
}

.prescription-card h2,
.advice-card h2 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #ff4757;
  font-size: 1.5rem;
}

.prescription-text {
  font-size: 1.4rem;
  line-height: 1.8;
  color: #ffa502;
  font-weight: 600;
  white-space: pre-wrap;
  text-align: center;
  padding: 1.5rem;
  background: rgba(255, 165, 2, 0.1);
  border-radius: 8px;
  border: 2px solid #ffa502;
  text-shadow: 0 0 10px rgba(255, 165, 2, 0.3);
}

.advice-text {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #dfe4ea;
  white-space: pre-wrap;
}

.footer {
  text-align: center;
  color: #747d8c;
  margin-top: 3rem;
}

.footer p {
  margin: 0.3rem 0;
}

.meme-credit {
  font-size: 0.85rem;
  font-style: italic;
}

@media (max-width: 768px) {
  .header h1 {
    font-size: 1.8rem;
  }

  .subtitle {
    font-size: 1.1rem;
  }

  .input-section,
  .prescription-card,
  .advice-card {
    padding: 1.5rem;
  }

  .button-group {
    flex-direction: column;
  }

  .prescription-text {
    font-size: 1.2rem;
  }
}
</style>
