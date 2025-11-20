"""
RAG Core Logic - 心靈處方籤機器人
基於 LangChain 和 FAISS 的檢索增強生成系統
支援多種 LLM：Groq (Llama)、Ollama (本地)、OpenAI
"""

import os
import numpy as np
from typing import Optional
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.schema import HumanMessage

# 心靈處方籤列表
SPIRITUAL_PRESCRIPTIONS = [
    "感謝給我們機會，順境、逆境，皆是恩人。",
    "身心常放鬆，逢人面帶笑；放鬆能使我們身心健康，帶笑容易增進彼此友誼。",
    "識人識己識進退，時時身心平安；知福惜福多培福，處處廣結善緣。",
    "平常心就是最自在、最愉快的心。",
    "知道自己的缺點愈多，成長的速度愈快，對自己的信心也就愈堅定。"
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
        # 抽取一條隨機的心靈處方籤
        chosen_prescription = np.random.choice(SPIRITUAL_PRESCRIPTIONS)
        
        # 自訂 prompt，結合心靈處方籤、書籍內容和使用者問題
        prompt = f"""你是一位充滿智慧的心靈導師。

使用者抽到了一個心靈處方籤：
「{chosen_prescription}」

以下是來自聖嚴法師《真正的快樂》一書的部分內容：
{_books_content[:3000]}

請根據這個心靈處方籤的智慧，結合書中的觀念，用溫暖、正面且具啟發性的語氣，回應使用者的煩惱。回答請控制在 200 字以內，給予實用的建議和鼓勵。

使用者的煩惱：
「{question}」

你的回應："""
        
        # 使用 LLM 生成回答
        final_response = _llm.invoke([HumanMessage(content=prompt)])
        
        return {
            "prescription": chosen_prescription,
            "advice": final_response.content
        }
        
    except Exception as e:
        print(f"處理問題時發生錯誤: {e}")
        return _get_fallback_response(question)


def _get_fallback_response(question: str) -> dict:
    """
    當 RAG 系統無法使用時的備用回應
    """
    chosen_prescription = np.random.choice(SPIRITUAL_PRESCRIPTIONS)
    
    return {
        "prescription": chosen_prescription,
        "advice": f"謝謝你分享你的煩惱：「{question}」。\n\n"
                  f"根據你抽到的處方籤「{chosen_prescription}」，"
                  f"希望這句話能為你帶來一些啟發。\n\n"
                  f"每個困難都是成長的機會，相信自己能夠克服當前的挑戰。"
                  f"不妨嘗試從不同角度看待問題，或許會有新的發現。"
    }
