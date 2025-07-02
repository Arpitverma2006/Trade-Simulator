# 💹 Django Trade Simulator

![Django](https://img.shields.io/badge/Django-4.x-green?logo=django)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![License](https://img.shields.io/github/license/yourusername/trade-simulator)
![Status](https://img.shields.io/badge/Status-In%20Development-orange)
![Stars](https://img.shields.io/github/stars/yourusername/trade-simulator?style=social)

## 📈 Project Overview

The **Django Trade Simulator** is a real-time, high-performance trading simulator designed to estimate **transaction costs**, **slippage**, and **market impact** using **Level-2 (L2) orderbook data** from OKX via WebSocket. The platform supports live data ingestion, graphical analysis, and statistical trade execution modeling.

---

## 🔧 Features

- 📡 Real-time L2 Orderbook via OKX WebSocket
- 🧠 Trade cost modeling: slippage, market impact, transaction cost
- 📊 Depth chart & trade visualization
- ⚙️ Maker vs Taker fee estimation
- 📁 Django Admin + Custom User Dashboard
- 📉 Backtest and simulate trades
- 🔐 Secure & modular Django architecture

---

## 🚀 Tech Stack

- **Frontend**: Tailwind CSS, Chart.js, HTMX (optional)
- **Backend**: Django, Django REST Framework
- **WebSocket Integration**: `websockets`, `channels`
- **Data Visualization**: Plotly / Chart.js
- **Database**: PostgreSQL
- **API**: OKX L2 Market Data WebSocket Feed

---

## 📷 Screenshots

> Add these images in the `/screenshots` folder of your repo.

| Dashboard Panel | Live Orderbook Feed | Trade Simulation |
|------------------|----------------------|-------------------|
| ![Dashboard](screenshots/dashboard.png) | ![Orderbook](screenshots/orderbook.png) | ![Simulator](screenshots/simulator.png) |

---

## 🧪 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/trade-simulator.git
   cd trade-simulator
