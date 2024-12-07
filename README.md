# NFP News Trading Bot for XAUUSD

## Overview
A specialized trading bot designed to analyze Non-Farm Payroll (NFP) news releases and their impact on XAUUSD (Gold) trading. The bot combines news sentiment analysis with technical indicators to generate trading signals.

## Key Features
- 🔍 Real-time NFP news monitoring and filtering
- 📊 Advanced sentiment analysis of news content
- 📈 Integration with TradingView for technical analysis
- 🚀 FastAPI backend for real-time signal processing
- 🔄 Automatic webhook integration
- 📱 Real-time notifications and alerts

## Technical Architecture
### Backend Components
- `news_trader.py`: Core news analysis engine
  - NFP news filtering
  - Sentiment analysis
  - Signal generation
  
- `main.py`: FastAPI server
  - Webhook endpoints
  - Real-time processing
  - API documentation

### TradingView Integration
- `news_trader.pine`: Custom Pine Script
  - Multi-timeframe analysis
  - News signal integration
  - Advanced entry detection
  - Risk management

## Installation

### Prerequisites
- Python 3.11+
- NewsAPI key
- TradingView account

### Setup
1. Clone the repository:
```bash
git clone https://github.com/yourusername/nfp-news-trading-bot.git
cd nfp-news-trading-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```env
NEWS_API_KEY=your_newsapi_key
TRADINGVIEW_WEBHOOK_URL=your_webhook_url
```

4. Start the server:
```bash
python main.py
```

## Usage

### API Endpoints
- `GET /`: Health check and status
- `GET /news/latest`: Get latest NFP news analysis and signals

### TradingView Setup
1. Import the Pine Script (`news_trader.pine`)
2. Configure webhook alerts
3. Set up your preferred risk parameters

## Trading Strategy
The bot specifically focuses on NFP (Non-Farm Payroll) news from the United States and its impact on XAUUSD:

1. **News Monitoring**
   - Filters for NFP-related news
   - Focuses on US employment data
   - Real-time news processing

2. **Signal Generation**
   - Sentiment analysis of news content
   - Impact score calculation
   - Technical confirmation

3. **Risk Management**
   - Dynamic stop loss
   - Take profit calculations
   - Position sizing

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer
This trading bot is for educational purposes only. Always perform your own analysis and trade at your own risk.
