from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

router = APIRouter(prefix="/openai", tags=["OpenAI"])

DEFAULT_MODEL = os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo")
DEFAULT_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
DEFAULT_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))

class QueryRequest(BaseModel):
    query: str
    model_name: Optional[str] = DEFAULT_MODEL
    temperature: Optional[float] = DEFAULT_TEMPERATURE
    max_tokens: Optional[int] = DEFAULT_MAX_TOKENS

class QueryResponse(BaseModel):
    response: str

def get_openai_api_key() -> str:
    """Get OpenAI API key from environment variable."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=400,
            detail="OpenAI API key not found. Please set OPENAI_API_KEY environment variable."
        )
    return api_key

@router.post("/query", response_model=QueryResponse)
async def query_openai(request: QueryRequest):
    try:
        api_key = get_openai_api_key()
        
        chat_model = ChatOpenAI(
            model_name=request.model_name,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            api_key=api_key
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI assistant."),
            ("user", "{query}")
        ])
        
        chain = prompt | chat_model | StrOutputParser()
        
        response = await chain.ainvoke({"query": request.query})
        
        return QueryResponse(response=response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 