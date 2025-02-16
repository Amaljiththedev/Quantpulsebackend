# QuantPulse Backend

QuantPulse Backend is a powerful API-driven backend system designed for real-time stock and crypto trading simulations. Built using Django and Django Channels, it supports AI-based trade predictions, real-time market data, and advanced trading analytics.

## 🚀 Features

- **User Authentication** (JWT-based login/signup with OTP verification)
- **Real-Time Market Data** (Binance API, Alpha Vantage integration)
- **Trading Engine** (Order execution, portfolio tracking, trade history)
- **AI-Powered Predictions** (LSTM/RNN models for price forecasting)
- **WebSockets for Live Updates**
- **Multi-Exchange Aggregation Support**
- **Advanced Reporting & Analytics**
- **Scalable Deployment on AWS (EC2, RDS, Redis, Docker, Kubernetes)**

## 🏗️ Tech Stack

- **Backend:** Django, Django Channels, Django REST Framework (DRF), Celery, Redis, PostgreSQL (TimescaleDB)
- **AI Models:** Scikit-Learn, TensorFlow/PyTorch (for trade predictions)
- **Infrastructure:** AWS EC2, RDS, Redis, Docker, Kubernetes, Cloudflare CDN
- **Data Sources:** Alpha Vantage, Binance API (real-time stock/crypto prices)

## 📌 Setup & Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Amaljiththedev/Quantpulsebackend.git
cd Quantpulsebackend
```

### 2️⃣ Set Up Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate     # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables
Create a `.env` file and set the required environment variables:
```
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/quantpulse_db
REDIS_URL=redis://localhost:6379
BINANCE_API_KEY=your-binance-api-key
ALPHA_VANTAGE_API_KEY=your-alpha-vantage-api-key
```

### 5️⃣ Run Database Migrations
```bash
python manage.py migrate
```

### 6️⃣ Start the Server
```bash
python manage.py runserver
```

## 🔗 API Endpoints
| Method | Endpoint | Description |
|--------|-----------------|---------------------------------|
| POST   | `/api/auth/register/` | Register a new user with OTP verification |
| POST   | `/api/auth/login/` | Authenticate user & return JWT token |
| POST   | `/api/trade/order/` | Execute a trade order |
| GET    | `/api/market/data/` | Fetch real-time market data |
| GET    | `/api/portfolio/` | Get user portfolio details |

## 🛠️ Running Tests
```bash
pytest
```

## 🚢 Deployment
### **Using Docker**
```bash
docker-compose up --build -d
```

### **Kubernetes Deployment**
```bash
kubectl apply -f kubernetes/deployment.yaml
```

## 📜 License
This project is licensed under the MIT License.

---
### 📬 Contact
For any queries or contributions, reach out to **Amaljith Thusharam Anil** at [your-email@example.com](mailto:your-email@example.com).

