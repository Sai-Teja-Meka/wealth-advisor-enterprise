# ============================================================
# DATA INGESTION SERVICE (Rune α)
# ============================================================

import requests
import os
from datetime import datetime
from typing import Dict, Any

class DataService:
    """Fetches real-time financial data from APIs"""
    
    def __init__(self):
        self.finnhub_key = os.getenv("FINNHUB_API_KEY")
        self.fmp_key = os.getenv("FMP_API_KEY")
        self.cache = {}
    
    def fetch_company_data(self, ticker: str) -> Dict[str, Any]:
        """Fetch complete company data"""
        try:
            # Get price
            price = self._fetch_price(ticker)
            name = self._fetch_name(ticker)
            ratios = self._fetch_ratios(ticker)
            
            return {
                "ticker": ticker,
                "name": name,
                "price": price,
                "pe_ratio": ratios.get("pe_ratio", 20),
                "profit_margin": ratios.get("profit_margin", 0.15),
                "roe": ratios.get("roe", 0.15),
                "debt_equity": ratios.get("debt_equity", 1.0),
                "current_ratio": ratios.get("current_ratio", 2.0),
                "revenue_growth": ratios.get("revenue_growth", 0.10),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            return None
    
    def _fetch_price(self, ticker: str) -> float:
        """Get stock price"""
        try:
            url = "https://finnhub.io/api/v1/quote"
            params = {"symbol": ticker, "token": self.finnhub_key}
            r = requests.get(url, params=params, timeout=5)
            return r.json().get("c", 0)
        except:
            return 0.0
    
    def _fetch_name(self, ticker: str) -> str:
        """Get company name"""
        try:
            url = "https://finnhub.io/api/v1/stock/profile2"
            params = {"symbol": ticker, "token": self.finnhub_key}
            r = requests.get(url, params=params, timeout=5)
            return r.json().get("name", ticker)
        except:
            return ticker
    
    def _fetch_ratios(self, ticker: str) -> Dict:
        """Get financial ratios"""
        try:
            url = f"https://financialmodelingprep.com/api/v3/financial-ratios-ttm/{ticker}"
            params = {"apikey": self.fmp_key}
            r = requests.get(url, params=params, timeout=5)
            data = r.json()
            
            if data and len(data) > 0:
                ratio = data
                return {
                    "pe_ratio": ratio.get("peRatioTTM", 20),
                    "profit_margin": ratio.get("netProfitMarginTTM", 0.15),
                    "roe": ratio.get("roeTTM", 0.15),
                    "debt_equity": ratio.get("debtToEquityTTM", 1.0),
                    "current_ratio": ratio.get("currentRatioTTM", 2.0),
                    "revenue_growth": 0.10
                }
        except:
            pass
        
        return {
            "pe_ratio": 20,
            "profit_margin": 0.15,
            "roe": 0.15,
            "debt_equity": 1.0,
            "current_ratio": 2.0,
            "revenue_growth": 0.10
        }
