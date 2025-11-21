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
    errorMessage.value = '請輸入你的煩惱'
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
    errorMessage.value = error.response?.data?.detail || '發生錯誤,請稍後再試'
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
      <h1>🧘‍♀️ 心靈處方籤</h1>
      <p class="subtitle">說出你的煩惱,讓 AI 為你指引方向</p>
    </header>

    <main class="main-content">
      <div class="input-section">
        <label for="question">你的煩惱:</label>
        <textarea
          id="question"
          v-model="userQuestion"
          placeholder="請描述你目前遇到的困擾或煩惱..."
          rows="5"
          :disabled="isLoading"
        ></textarea>

        <div class="button-group">
          <button 
            @click="getPrescription" 
            :disabled="isLoading"
            class="btn-primary"
          >
            {{ isLoading ? '求籤中...' : '🙏 求籤' }}
          </button>
          <button 
            @click="reset" 
            :disabled="isLoading"
            class="btn-secondary"
          >
            重置
          </button>
        </div>

        <div v-if="errorMessage" class="error-message">
          ⚠️ {{ errorMessage }}
        </div>
      </div>

      <div v-if="prescription || advice" class="result-section">
        <div class="prescription-card">
          <h2>📜 籤詩</h2>
          <div class="prescription-text">
            {{ prescription }}
          </div>
        </div>

        <div class="advice-card">
          <h2>🤖 AI 解籤</h2>
          <div class="advice-text">
            {{ advice }}
          </div>
        </div>
      </div>
    </main>

    <footer class="footer">
      <p>Powered by RAG Technology & AI</p>
    </footer>
  </div>
</template>

<style scoped>
* {
  box-sizing: border-box;
}

.app-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.header {
  text-align: center;
  color: white;
  margin-bottom: 2rem;
}

.header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
}

.main-content {
  max-width: 800px;
  margin: 0 auto;
}

.input-section {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  margin-bottom: 2rem;
}

label {
  display: block;
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #333;
}

textarea {
  width: 100%;
  padding: 1rem;
  font-size: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  resize: vertical;
  font-family: inherit;
  transition: border-color 0.3s;
}

textarea:focus {
  outline: none;
  border-color: #667eea;
}

textarea:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: #f5f5f5;
  color: #666;
}

.btn-secondary:hover:not(:disabled) {
  background: #e0e0e0;
}

.error-message {
  margin-top: 1rem;
  padding: 1rem;
  background: #fee;
  color: #c33;
  border-radius: 8px;
  border-left: 4px solid #c33;
}

.result-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.prescription-card,
.advice-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.prescription-card h2,
.advice-card h2 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #667eea;
  font-size: 1.5rem;
}

.prescription-text {
  font-size: 1.3rem;
  line-height: 1.8;
  color: #333;
  font-weight: 500;
  white-space: pre-wrap;
  text-align: center;
  padding: 1rem;
  background: #f9f9f9;
  border-radius: 8px;
  border: 2px solid #667eea;
}

.advice-text {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #555;
  white-space: pre-wrap;
}

.footer {
  text-align: center;
  color: white;
  margin-top: 3rem;
  opacity: 0.8;
}

@media (max-width: 768px) {
  .header h1 {
    font-size: 2rem;
  }

  .input-section,
  .prescription-card,
  .advice-card {
    padding: 1.5rem;
  }

  .button-group {
    flex-direction: column;
  }
}
</style>
