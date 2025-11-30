"""
RAG Core Logic - 小明劍魔 AI 吐槽系統
基於 LangChain 和 FAISS 的檢索增強生成系統
支援多種 LLM：Groq (Llama)、Ollama (本地)、OpenAI

⚔️ 小明劍魔迷因版 - 諷刺風格 AI 顧問
靈感來源：B站實況主小明劍魔的經典語錄
"""

import os
import numpy as np
from typing import Optional
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.messages import HumanMessage

# ⚔️ 劍魔語錄
SWORD_DEMON_QUOTES = [
    "怎麼不找找自己的問題？",
    "你爸得了MVP，你媽就是躺贏狗！",
    "他們不解決問題，他們解決你！",
    "我只能戰死，不能躺平被推死！",
    "評分系統把人的付出異化掉了，懂嗎？",
    "你太出格，你太激進！",
    "輸了還不能說？輸了還不能有情緒？",
    "我真的很佩服這個設計師，他媽的，這東西設計得剛剛好，真的就是剛剛好，唉這真的是智慧啊，剛剛好你吃飯又餓不死。",
    "你告訴我怎麼贏，啊？你排群傻逼給我怎麼贏",
    "嗯你回答我？你們這些人回答我！Look at my eyes , tell me why , why baby why?"
]

# 全域變數，用於儲存已初始化的系統
_llm = None
_is_initialized = False
_llm_provider = None  # 'gemini', 'groq', 'ollama', 'openai', 或 None


def _initialize_llm():
    """
    初始化 LLM，自動檢測可用的提供商
    優先順序：Gemini (免費) > Groq (免費) > Ollama (本地) > OpenAI (付費)
    """
    global _llm, _llm_provider
    
    # 1. 嘗試使用 Google Gemini(免費，每天大額度)
    if os.getenv("GOOGLE_API_KEY"):
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            _llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",  # 快速輕量模型
                temperature=0.7,
                api_key=os.getenv("GOOGLE_API_KEY")
            )
            _llm_provider = "gemini"
            print("✓ 使用 Google Gemini 2.5 Flash")
            return
        except ImportError:
            print("提示：安裝 langchain-google-genai 以使用 Gemini")
        except Exception as e:
            print(f"Gemini 初始化失敗: {e}")
    
    # 2. 嘗試使用 Groq(免費，速度快)
    if os.getenv("GROQ_API_KEY"):
        try:
            from langchain_groq import ChatGroq
            _llm = ChatGroq(
                model="llama-3.1-70b-versatile",  # 或 mixtral-8x7b-32768
                temperature=0.7
            )
            _llm_provider = "groq"
            print("✓ 使用 Groq (Llama 3.1 70B)")
            return
        except ImportError:
            print("提示：安裝 langchain-groq 以使用 Groq")
        except Exception as e:
            print(f"Groq 初始化失敗: {e}")
    
    # 2. 嘗試使用 Ollama（本地免費）
    try:
        from langchain_community.llms import Ollama
        # 測試連接
        test_llm = Ollama(model="llama3.1")  # 或 llama2, mistral 等
        test_llm.invoke("test")
        _llm = test_llm
        _llm_provider = "ollama"
        print("✓ 使用 Ollama (本地模型)")
        return
    except Exception as e:
        print(f"Ollama 不可用: {e}")
    
    # 3. 嘗試使用 OpenAI（付費）
    if os.getenv("OPENAI_API_KEY"):
        try:
            from langchain.chat_models import ChatOpenAI
            _llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
            _llm_provider = "openai"
            print("✓ 使用 OpenAI (GPT-4)")
            return
        except Exception as e:
            print(f"OpenAI 初始化失敗: {e}")
    
    # 5. 都不可用
    raise ValueError(
        "無法初始化任何 LLM！請設定以下其中一個：\n"
        "1. GOOGLE_API_KEY (推薦，免費) - https://makersuite.google.com/app/apikey\n"
        "2. GROQ_API_KEY (免費) - https://console.groq.com\n"
        "3. 安裝並啟動 Ollama (本地免費) - https://ollama.ai\n"
        "4. OPENAI_API_KEY (付費) - https://platform.openai.com"
    )


def _initialize_embeddings():
    """
    初始化 Embeddings，根據可用的服務自動選擇
    優先順序：Gemini > OpenAI > Ollama
    """
    # 1. 如果使用 Gemini，使用 Google embeddings
    if os.getenv("GOOGLE_API_KEY"):
        try:
            from langchain_google_genai import GoogleGenerativeAIEmbeddings
            print("✓ 使用 Google Embeddings")
            return GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        except ImportError:
            print("提示：安裝 langchain-google-genai 以使用 Google embeddings")
        except Exception as e:
            print(f"Google embeddings 初始化失敗: {e}")
    
    # 2. 使用 OpenAI Embeddings（需要 API Key）
    if os.getenv("OPENAI_API_KEY"):
        try:
            from langchain.embeddings.openai import OpenAIEmbeddings
            print("✓ 使用 OpenAI Embeddings")
            return OpenAIEmbeddings()
        except Exception as e:
            print(f"OpenAI embeddings 初始化失敗: {e}")
    
    # 3. 嘗試使用 Ollama Embeddings（本地免費）
    try:
        from langchain_community.embeddings import OllamaEmbeddings
        print("✓ 使用 Ollama Embeddings")
        return OllamaEmbeddings(model="nomic-embed-text")
    except Exception as e:
        print(f"Ollama embeddings 不可用: {e}")
    
    raise ValueError("無法初始化 Embeddings！請設定 GOOGLE_API_KEY、OPENAI_API_KEY 或安裝 Ollama")


# 全域變數儲存書籍內容
_books_content = ""

def initialize_rag_system(books_dir: str = "books", force_reload: bool = False):
    """
    初始化 RAG 系統，載入書籍內容和語言模型
    
    Args:
        books_dir: 書籍文件所在的資料夾路徑
        force_reload: 是否強制重新載入
    """
    global _llm, _is_initialized, _books_content
    
    if _is_initialized and not force_reload:
        return
    
    print("正在初始化 RAG 系統...")
    
    # 檢查資料夾是否存在
    if not os.path.exists(books_dir):
        print(f"警告: 資料夾 '{books_dir}' 不存在，將使用預設回應")
        _is_initialized = False
        return
    
    try:
        # Step 1: 直接載入文件內容（不使用 embeddings）
        loader = DirectoryLoader(
            books_dir, 
            glob="**/*.txt",
            loader_cls=TextLoader,
            loader_kwargs={'autodetect_encoding': True}
        )
        documents = loader.load()
        
        if not documents:
            print(f"警告: 資料夾 '{books_dir}' 中沒有找到 .txt 文件")
            _is_initialized = False
            return
        
        # Step 2: 合併所有文件內容（取前10000字，避免太長）
        _books_content = "\n\n".join([doc.page_content for doc in documents])
        _books_content = _books_content[:10000]  # 限制長度
        
        # Step 3: 初始化語言模型
        _initialize_llm()
        
        _is_initialized = True
        print(f"✓ RAG 系統初始化完成！載入了 {len(documents)} 個文件（{len(_books_content)} 字）。")
        
    except Exception as e:
        print(f"初始化 RAG 系統時發生錯誤: {e}")
        _is_initialized = False
        raise


def get_ai_response(question: str) -> dict:
    """
    處理使用者問題並返回心靈處方籤與 AI 建議
    
    Args:
        question: 使用者的煩惱或問題
        
    Returns:
        dict: 包含 prescription (籤詩) 和 advice (AI 建議) 的字典
    """
    global _llm, _is_initialized, _books_content
    
    # 如果系統未初始化，嘗試初始化
    if not _is_initialized:
        try:
            initialize_rag_system()
        except Exception as e:
            print(f"無法初始化 RAG 系統: {e}")
            return _get_fallback_response(question)
    
    # 如果初始化失敗，返回備用回應
    if not _is_initialized or not _llm:
        return _get_fallback_response(question)
    
    try:
        # 抽取一條隨機的劍魔語錄
        chosen_quote = np.random.choice(SWORD_DEMON_QUOTES)
        
        # ⚔️ 劍魔風格 prompt，諷刺式 AI 吐槽
        prompt = f"""你是「小明劍魔」，一個充滿諷刺和黑色幽默的 AI 吐槽系統。

你的風格特點：
- 用誇張的方式把使用者的問題延伸到社會議題
- 諷刺「找自己問題」這種把系統問題歸咎於個人的邏輯
- 帶有憤怒但又幽默的語氣
- 最後給一點真正有用的建議（用諷刺包裝）

使用者抽到的劍魔語錄：
「{chosen_quote}」

使用者的煩惱：
「{question}」

請用小明劍魔的風格回應，包含以下結構：
1. 先用「怎麼不找找自己的問題？」的邏輯諷刺一番（2-3句話）
2. 把問題延伸到荒謬的社會現象（2-3句話）
3. 最後給一個真正有意義的建議（用諷刺語氣包裝）

回答請控制在 200 字以內。記住：你是在用黑色幽默幫助使用者，不是真的在罵人！

你的回應："""
        
        # 使用 LLM 生成回答
        final_response = _llm.invoke([HumanMessage(content=prompt)])
        
        return {
            "prescription": chosen_quote,
            "advice": final_response.content
        }
        
    except Exception as e:
        print(f"處理問題時發生錯誤: {e}")
        return _get_fallback_response(question)


def _get_fallback_response(question: str) -> dict:
    """
    當 RAG 系統無法使用時的備用回應（劍魔風格）
    """
    chosen_quote = np.random.choice(SWORD_DEMON_QUOTES)
    
    return {
        "prescription": chosen_quote,
        "advice": f"你說你的煩惱是：「{question}」？\n\n"
                  f"怎麼不找找自己的問題？為什麼別人沒有這個煩惱？"
                  f"為什麼就你特別倒楣？全部找自己的問題好不好？\n\n"
                  f"⚔️ 劍魔語錄：「{chosen_quote}」\n\n"
                  f"好啦不開玩笑了，系統現在有點問題（對，是系統的問題不是你的問題），"
                  f"但記住：有些事真的不是你的錯，別什麼都往自己身上扛。"
    }
