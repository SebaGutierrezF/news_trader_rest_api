import requests
from textblob import TextBlob
import time
from datetime import datetime, timedelta
import json
import os
from dotenv import load_dotenv
import logging
from newsapi import NewsApiClient
import pandas as pd

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('news_trader.log'),
        logging.StreamHandler()
    ]
)

class NewsTrader:
    def __init__(self):
        """Inicializa el trader con la API key desde las variables de entorno"""
        load_dotenv()
        self.api_key = os.getenv('NEWS_API_KEY')
        if not self.api_key:
            raise ValueError("NEWS_API_KEY no encontrada en variables de entorno")
        self.newsapi = NewsApiClient(api_key=self.api_key)
        self.sentiment_threshold = 0.3
        self.tradingview_webhook = os.getenv('TRADINGVIEW_WEBHOOK_URL', 'YOUR_WEBHOOK_URL')

    def is_nfp_news(self, article):
        """Verifica si la noticia está relacionada con NFP de EEUU"""
        nfp_keywords = [
            'non-farm payroll', 'nonfarm payroll', 'non farm payroll', 'nfp',
            'us employment', 'u.s. employment', 'us jobs report', 'u.s. jobs report',
            'us labor market', 'u.s. labor market'
        ]
        
        title = article.get('title', '').lower()
        description = article.get('description', '').lower()
        content = article.get('content', '').lower()
        
        # Verificar que sea de EEUU
        us_indicators = ['united states', 'u.s.', 'us ', 'usa', 'america']
        is_us_related = any(indicator in title + ' ' + description + ' ' + content 
                          for indicator in us_indicators)
        
        # Verificar que sea relacionado con NFP
        is_nfp_related = any(keyword in title + ' ' + description + ' ' + content 
                           for keyword in nfp_keywords)
        
        return is_us_related and is_nfp_related

    def send_to_tradingview(self, signal_value):
        """Envía la señal a TradingView mediante webhook"""
        try:
            payload = {
                'value': signal_value,
                'timestamp': datetime.now().isoformat(),
                'key': 'news_signal'  # Identificador para TradingView
            }
            
            # Escribir la señal en un archivo que TradingView puede leer
            with open('news_signal.txt', 'w') as f:
                json.dump(payload, f)
            
            logging.info(f"Señal guardada: {signal_value}")
            
        except Exception as e:
            logging.error(f"Error enviando señal a TradingView: {e}")

    def analyze_sentiment(self, text):
        """Analiza el sentimiento de un texto usando TextBlob"""
        try:
            if not text or not isinstance(text, str):
                logging.warning(f"Texto inválido para análisis de sentimiento: {text}")
                return 0
            analysis = TextBlob(text)
            return analysis.sentiment.polarity
        except Exception as e:
            logging.error(f"Error en análisis de sentimiento: {e}")
            return 0

    def calculate_impact_score(self, article):
        """Calcula un score de impacto basado en varios factores"""
        # Si no es noticia de NFP, retornar 0
        if not self.is_nfp_news(article):
            return 0
            
        title = article.get('title', '')
        description = article.get('description', '')
        
        # Verificar que tengamos al menos título o descripción
        if not title and not description:
            logging.warning("Artículo sin título ni descripción")
            return 0
            
        title_sentiment = self.analyze_sentiment(title)
        desc_sentiment = self.analyze_sentiment(description)
        
        weights = {
            'title': 0.6,
            'description': 0.4
        }
        
        impact_score = (
            title_sentiment * weights['title'] +
            desc_sentiment * weights['description']
        )
        
        # Escribir la señal y descripción en un archivo
        try:
            with open('news_signal.txt', 'w') as f:
                f.write(f"{impact_score}|{title}|{description}")
            logging.info(f"Señal NFP escrita en archivo: {impact_score}")
        except Exception as e:
            logging.error(f"Error escribiendo señal: {e}")
        
        return impact_score

    def process_news(self):
        """Procesa las últimas noticias y genera señales de trading"""
        try:
            # Obtener noticias de las últimas 24 horas
            from_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            
            news = self.newsapi.get_everything(
                q='employment OR jobs OR labor OR payroll',
                language='en',
                from_param=from_date,
                sort_by='relevancy'
            )
            
            max_impact = 0
            for article in news['articles']:
                impact = self.calculate_impact_score(article)
                if abs(impact) > abs(max_impact):
                    max_impact = impact
            
            logging.info(f"Impacto máximo de NFP: {max_impact}")
            self.send_to_tradingview(max_impact)
            return max_impact
            
        except Exception as e:
            logging.error(f"Error procesando noticias: {e}")
            return 0

    def run(self, interval=300):
        """Ejecuta el trader en un loop continuo"""
        logging.info("Iniciando News Trader...")
        
        while True:
            try:
                impact_score = self.process_news()
                logging.info(f"Score máximo de impacto: {impact_score:.2f}")
                time.sleep(interval)
                
            except Exception as e:
                logging.error(f"Error en el loop principal: {e}")
                time.sleep(60)

if __name__ == "__main__":
    trader = NewsTrader()
    trader.run()
