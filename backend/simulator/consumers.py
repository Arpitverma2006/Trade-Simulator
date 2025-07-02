import json
import time
import asyncio
import websockets
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import (
    estimate_slippage,
    estimate_fee,
    estimate_market_impact,
    predict_maker_taker
)

class MarketDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.symbol = "BTC-USDT-SWAP"
        self.url = f"wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/{self.symbol}"
        self.keep_running = True
        asyncio.create_task(self.receive_orderbook())

    async def disconnect(self, close_code):
        self.keep_running = False

    async def receive_orderbook(self):
        try:
            async with websockets.connect(self.url) as ws:
                while self.keep_running:
                    tick_start = time.perf_counter()
                    raw_data = await ws.recv()
                    data = json.loads(raw_data)
                    parse_time = time.perf_counter()
                    # Parse price levels from orderbook
                    price_levels = [[27000.1, 0.1], [27000.3, 0.15], [27000.7, 0.2]]  # Example L2 orderbook
                    fee_tier = "tier_1"  # Or extracted from data
                    volatility = 0.5  # Or extracted from data
                    quantity = 100
                    start_time = time.time()  
                    # Parse quantity safely
                    try:
                        quantity = float(data.get("quantity", 100))  # from frontend JSON or default
                    except (ValueError, TypeError):
                        quantity = 100

                    # Correct call
                    try:
                        slippage_pct = estimate_slippage(price_levels, quantity)
                    except Exception as e:
                        slippage_pct = None
                        error = f"Slippage estimation failed: {e}"


                    # Simulate internal models
                    quantity = 1.0  # or dynamically set based on user input or default value
                    # slippage_pct = estimate_slippage(data, quantity)
                    # slippage_pct = estimate_slippage(price_levels, quantity)
                    slippage_pct = estimate_slippage(price_levels, quantity)
                    fees = estimate_fee(fee_tier, quantity)
                    market_impact = estimate_market_impact(volatility, quantity)
                    maker_taker_prob = predict_maker_taker(slippage_pct)
                    net_cost = fees + market_impact
                    latency = round((time.time() - start_time) * 1000, 2)

                    # await self.send(text_data=json.dumps({
                    #     "exchange": data["exchange"],
                    #     "symbol": data["symbol"],
                    #     "timestamp": data["timestamp"],
                    #     "latency_ms": round(latency, 2),
                    #     "model_latency_ms": round(model_latency, 2),
                    #     "slippage_pct": round(slippage_pct, 4),
                    #     "fees": round(fees, 4),
                    #     "impact": round(impact, 4),
                    #     "net_cost": round(slippage_pct + fees + impact, 4),
                    #     "taker_probability": round(taker_prob, 2)
                    # }))
                    # await self.send(text_data=json.dumps({
                    #     "exchange": data["exchange"],
                    #     "symbol": data["symbol"],
                    #     "timestamp": data["timestamp"],
                    #     "bids": data["bids"][:5],
                    #     "asks": data["asks"][:5],
                    #     "latency_ms": round(latency, 2),
                    #     "slippage_pct": round(slippage_pct, 4),
                    #     "fees": round(fees, 4),
                    #     "impact": round(impact, 4),
                    #     "net_cost": round(slippage_pct + fees + impact, 4),
                    #     "taker_probability": round(taker_prob, 2)
                    # }))
                    await self.send(text_data=json.dumps({
                        "slippage_pct": slippage_pct,
                        "fees_usd": fees,
                        "market_impact_usd": market_impact,
                        "net_cost_usd": net_cost,
                        "maker_taker_prob": maker_taker_prob,
                        "latency_ms": latency
                    }))


        except Exception as e:
            await self.send(text_data=json.dumps({"error": str(e)}))


# from channels.generic.websocket import AsyncWebsocketConsumer
# import json

# class MarketDataConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()  # Accept the WebSocket connection

#     async def disconnect(self, close_code):
#         pass  # Handle disconnect if needed

#     async def receive(self, text_data=None, bytes_data=None):
#         # Example: Echo back received data or handle messages
#         await self.send(text_data=json.dumps({"message": "Hello from server!"}))
