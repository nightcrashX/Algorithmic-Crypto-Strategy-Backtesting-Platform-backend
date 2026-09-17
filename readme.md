# 🚀 Crypto Trading & Market Analytics Platform — Backend

A scalable **FastAPI backend** for a cryptocurrency trading and market analytics platform. The backend provides real-time market data, exchange integration, technical indicators, chart data, authentication, demo trading, portfolio management, trade history, and real-time WebSocket updates.

The architecture is designed to keep **business logic, market-data processing, calculations, and database operations on the backend**, while the frontend focuses primarily on visualization and user interaction.

---

## 📌 Overview

This backend powers a TradingView-inspired cryptocurrency trading platform where users can:

* View real-time cryptocurrency market data
* Access OHLCV/candlestick data
* Analyze charts using technical indicators
* Switch between supported exchanges
* Switch symbols and timeframes dynamically
* Receive live candle updates through WebSockets
* Place demo buy/sell orders
* Track portfolio balance and positions
* Monitor profit & loss
* View trade/order history
* Authenticate securely using JWT
* Store user and trading data in MongoDB

> **Note:** Strategy creation and backtesting UI sections are planned for future development. The current backend focuses on market data, technical analysis, demo trading, portfolio, and related services.

---

# 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │      Frontend        │
                         │   React + Vite       │
                         └──────────┬───────────┘
                                    │
                         REST APIs / WebSocket
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      FastAPI         │
                         │      Backend         │
                         └──────────┬───────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
             ▼                      ▼                      ▼
      ┌─────────────┐       ┌─────────────┐       ┌─────────────┐
      │ Exchange    │       │ Technical   │       │ Trading     │
      │ Integration │       │ Indicators  │       │ Services    │
      │    CCXT     │       │ Calculation │       │             │
      └──────┬──────┘       └─────────────┘       └──────┬──────┘
             │                                             │
             ▼                                             ▼
      ┌─────────────┐                              ┌─────────────┐
      │ Exchanges   │                              │  MongoDB    │
      │ Binance     │                              │   Atlas     │
      │ Delta       │                              └─────────────┘
      │ Others      │
      └─────────────┘
```

---

# ⚡ Key Features

## 📊 Market Data

The backend provides cryptocurrency market information through exchange APIs.

Supported functionality includes:

* OHLCV data
* Candlestick data
* Current market prices
* Symbol information
* Exchange information
* Timeframe-based data
* Historical chart data
* Paginated chart data

Exchange communication is handled through **CCXT**, allowing the backend to work with multiple cryptocurrency exchanges through a unified interface.

---

## 📈 Technical Indicators

Technical indicators are calculated on the **backend** rather than the frontend.

This provides:

* Consistent calculations
* Centralized business logic
* Reduced frontend processing
* Dynamic indicator configuration
* Exchange/symbol/timeframe compatibility
* Easier maintenance

Examples of supported indicators include:

* SMA
* EMA
* RSI
* MACD
* Bollinger Bands
* Supertrend
* Volume-based indicators
* Other technical-analysis indicators

The frontend receives calculated indicator values and is responsible primarily for rendering them on the chart.

---

# 🔴 Real-Time Market Data

The backend uses **WebSockets** for real-time market updates.

Example:

```text
WebSocket
ws://localhost:8000/live/ws/candles/{exchange}/{symbol}/{timeframe}
```

Example:

```text
ws://localhost:8000/live/ws/candles/binance/BTCUSDT/15m
```

The WebSocket layer can provide:

* Live candles
* Updated OHLC values
* Real-time price changes
* Dynamic symbol updates
* Dynamic timeframe updates

---

# 📉 Chart Data & Pagination

Historical chart data is handled by the backend.

Instead of loading a large amount of historical data at once, the backend supports pagination so the frontend can request chart data in smaller chunks.

Conceptually:

```text
Frontend
   │
   │ Request historical candles
   ▼
Backend
   │
   │ Fetch / process requested range
   ▼
Exchange / Cache / Data Source
   │
   ▼
Backend
   │
   │ Paginated response
   ▼
Frontend Chart
```

This approach helps improve:

* Initial chart loading
* Network performance
* Memory usage
* Chart responsiveness

---

# 💱 Exchange Integration

The backend uses **CCXT** to communicate with cryptocurrency exchanges.

CCXT provides a unified interface for exchange operations such as:

```text
Exchange
   │
   ├── Markets
   ├── Symbols
   ├── OHLCV
   ├── Tickers
   └── Trading APIs
```

The backend can dynamically work with different:

* Exchanges
* Trading pairs
* Timeframes

The frontend does not need to directly communicate with individual exchange APIs for core market-data processing.

---

# 💰 Demo Trading

The platform includes a demo trading system for simulated trading.

Users can:

* Buy assets
* Sell assets
* Specify quantity
* Track executed trades
* Monitor available balance
* Track portfolio positions
* Calculate profit/loss

A demo account starts with virtual capital.

Example:

```text
Initial Demo Capital
        │
        ▼
   $10,000 Virtual
        │
   ┌────┴────┐
   ▼         ▼
  BUY       SELL
   │         │
   └────┬────┘
        ▼
 Portfolio
        │
        ▼
 Profit / Loss
```

No real-money orders are placed by the demo trading system.

---

# 📁 Trade History

Trade information is stored in MongoDB.

Trade records can contain information such as:

```text
Trade Type
Exchange
Symbol
Quantity
Price
Date
Time
Account Type
```

The backend also supports trade-history retrieval with:

* Pagination
* Date filtering
* Account filtering
* Historical trade records

---

# 💼 Portfolio Management

The portfolio system tracks the user's demo trading account.

It can maintain information such as:

* Available balance
* Asset holdings
* Entry price
* Current price
* Position quantity
* Unrealized P&L
* Realized P&L
* Portfolio value

The backend calculates portfolio-related values so the frontend can display them in real time.

---

# 📊 Live Profit & Loss

The backend supports calculating the current position's profit/loss using the latest market price.

Conceptually:

```text
Current Price
      │
      ▼
Position Data
      │
      ▼
P&L Calculation
      │
      ▼
Frontend
```

This allows the trading interface to display dynamic P&L as the market moves.

---

# 🔐 Authentication & Security

The backend uses JWT-based authentication.

Authentication flow:

```text
User
 │
 ▼
Login
 │
 ▼
FastAPI
 │
 ├── Verify credentials
 │
 └── Generate JWT
       │
       ▼
    Client
       │
       ▼
Authenticated API Requests
```

Security features include:

* JWT authentication
* Password hashing
* HTTP-only authentication cookie support
* Protected API routes
* Token expiration
* MongoDB-backed user management

---

# 🗄️ Database

The project uses **MongoDB / MongoDB Atlas** as the primary database.

Main data areas include:

```text
MongoDB
│
├── Users
├── Trades
├── Portfolios
├── Orders
└── Other application data
```

MongoDB is used because of its flexible document-based structure and suitability for rapidly evolving trading-platform data models.

---

# 📂 Backend Structure

A simplified project structure:

```text
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── routes/
│   │   ├── auth/
│   │   ├── market/
│   │   ├── indicator/
│   │   ├── trade/
│   │   ├── portfolio/
│   │   └── ...
│   │
│   ├── services/
│   │   ├── market_service.py
│   │   ├── indicator_service.py
│   │   ├── trade_service.py
│   │   └── ...
│   │
│   ├── schemas/
│   │   ├── trade_schema.py
│   │   ├── user_schema.py
│   │   └── ...
│   │
│   ├── database/
│   │   └── ...
│   │
│   └── utils/
│       └── ...
│
├── requirements.txt
├── .env
└── README.md
```

> The exact folder structure may differ depending on the current implementation.

---

# 🛠️ Tech Stack

### Backend

* **Python**
* **FastAPI**
* **Uvicorn**
* **Pydantic**

### Market Data

* **CCXT**
* Exchange APIs
* WebSockets

### Database

* **MongoDB**
* **MongoDB Atlas**

### Authentication

* **JWT**
* **bcrypt**
* Password hashing
* HTTP-only cookies

### API

* REST APIs
* WebSocket APIs

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone <YOUR_BACKEND_REPOSITORY_URL>
cd backend
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the backend root directory.

Example:

```env
MONGO_URI=your_mongodb_connection_string

JWT_SECRET=your_secret_key

JWT_ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

> Never commit `.env` or private API credentials to GitHub.

Add this to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

---

# ▶️ Running the Server

Start the FastAPI server:

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at:

```text
http://localhost:8000
```

---

# 📚 API Documentation

FastAPI automatically provides interactive API documentation.

### Swagger UI

```text
http://localhost:8000/docs
```


Swagger can be used to test:

* Authentication APIs
* Market APIs
* Chart APIs
* Indicator APIs
* Trading APIs
* Portfolio APIs
* Trade-history APIs

---

# 🔌 API Flow

A typical chart request:

```text
Frontend
   │
   │ Exchange + Symbol + Timeframe
   ▼
FastAPI
   │
   ▼
Market Service
   │
   ▼
CCXT / Exchange
   │
   ▼
OHLCV Data
   │
   ▼
Indicator Service
   │
   ▼
Calculated Indicators
   │
   ▼
API Response
   │
   ▼
Frontend Chart
```

---

# 📡 Real-Time Trading Flow

```text
Exchange WebSocket
        │
        ▼
Backend WebSocket Service
        │
        ├── Live Price
        ├── Candle Updates
        └── Market Updates
        │
        ▼
Frontend WebSocket Client
        │
        ▼
Trading Dashboard
```

---

# 🧮 Backend-First Architecture

One of the main architectural principles of this project is:

> **Business logic belongs to the backend.**

The backend handles:

* Market-data processing
* Indicator calculations
* Trading calculations
* Portfolio calculations
* P&L calculations
* Authentication
* Database operations
* Exchange integration

The frontend primarily handles:

* UI
* Chart rendering
* User interaction
* Data visualization

This separation makes the system easier to maintain and extend.

---

# 🚧 Future Development

Planned features include:

* [ ] Strategy Builder
* [ ] Backtesting Engine
* [ ] Strategy Management APIs
* [ ] Historical Backtesting
* [ ] Strategy Performance Metrics
* [ ] Advanced Portfolio Analytics
* [ ] More Technical Indicators
* [ ] Redis-based market-data caching
* [ ] Advanced order types
* [ ] Paper trading improvements
* [ ] AI-assisted market analysis
* [ ] Production-grade monitoring
* [ ] Rate-limit management
* [ ] Background task processing

---

# 🎯 Project Goals

The long-term goal is to build a complete cryptocurrency trading ecosystem with:

```text
                 Crypto Platform
                       │
       ┌───────────────┼───────────────┐
       │               │               │
    Markets         Trading        Analytics
       │               │               │
       ▼               ▼               ▼
   Live Data       Demo Trade     Indicators
   Charts          Portfolio      P&L
   Exchanges       History        Insights
                       │
                       ▼
                Future Extensions
                       │
              ┌────────┴────────┐
              ▼                 ▼
         Strategies        Backtesting
```

---

# 👨‍💻 Development

This project was developed as a full-stack cryptocurrency trading platform with a strong focus on:

* Backend architecture
* Real-time systems
* API development
* Exchange integration
* Technical analysis
* Database design
* WebSocket communication
* Trading-system logic

---

# 📄 License

This project is currently developed for educational and development purposes.

Add an appropriate open-source license before distributing the project publicly.

---

## ⭐ Acknowledgements

Built using:

* FastAPI
* Python
* CCXT
* MongoDB
* WebSockets
* Cryptocurrency exchange APIs

---

## ⚠️ Disclaimer

This project is intended for **educational and development purposes**. Cryptocurrency markets involve significant financial risk. The demo trading functionality does not represent real-money trading unless explicitly integrated with a live exchange and appropriately secured.
