from fastapi import FastAPI
import yfinance as yf
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for React Native requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/stocks/")
async def get_stock_data(symbols: str):
    stock_list = symbols.split(",")
    stock_data = []

    for symbol in stock_list:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1d")

        if not hist.empty:
            stock_data.append({
                "symbol": symbol,
                "price": hist["Close"].iloc[-1],
                "change": hist["Close"].iloc[-1] - hist["Open"].iloc[-1],
                "changePercent": ((hist["Close"].iloc[-1] - hist["Open"].iloc[-1]) / hist["Open"].iloc[-1]) * 100,
                "date": hist.index[-1].strftime("%Y-%m-%d")
            })

    return stock_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
