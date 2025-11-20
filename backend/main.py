from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_core import get_ai_response, initialize_rag_system
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Mind Healer API")

# 在應用啟動時初始化 RAG 系統
@app.on_event("startup")
async def startup_event():
    print("\n" + "="*50)
    print("🧘‍♀️ Mind Healer API 正在啟動...")
    print("="*50)
    
    # 讀取環境變數
    books_dir = os.getenv("BOOKS_DIR", "books")
    
    try:
        initialize_rag_system(books_dir=books_dir)
        print("✓ RAG 系統初始化成功\n")
    except Exception as e:
        print(f"⚠️ RAG 系統初始化失敗: {e}")
        print("⚠️ 將使用備用回應模式\n")

# CORS configuration to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    prescription: str
    advice: str


@app.get("/")
async def root():
    from rag_core import _is_initialized
    return {
        "message": "Mind Healer API is running",
        "status": "healthy",
        "rag_initialized": _is_initialized
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    接收使用者的煩惱，返回籤詩與 AI 建議
    """
    try:
        result = get_ai_response(request.question)
        return ChatResponse(
            prescription=result["prescription"],
            advice=result["advice"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"處理請求時發生錯誤: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
