from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from news_trader import NewsTrader
import os
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('news_trader.log'),
        logging.StreamHandler()
    ]
)

# Cargar variables de entorno
load_dotenv()

app = FastAPI(title="News Trading API")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar el trader
news_trader = NewsTrader()

@app.get("/")
async def root():
    return {"status": "active", "message": "News Trading API is running"}

@app.get("/news/latest")
async def get_latest_news():
    try:
        impact_score = news_trader.process_news()
        return {
            "status": "success",
            "impact_score": impact_score,
            "message": "NFP news processed successfully"
        }
    except Exception as e:
        logging.error(f"Error processing news: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
