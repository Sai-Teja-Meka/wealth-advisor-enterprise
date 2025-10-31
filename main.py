# ============================================================
# MAIN FASTAPI APPLICATION
# ============================================================

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import json
class TickerList(BaseModel):
    tickers: List[str]
load_dotenv()

app = FastAPI(
    title="Wealth Advisor Enterprise API",
    description="Multi-user investment advisory system",
    version="1.0.0"
)

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from backend.data_service import DataService
from backend.analysis_service import AnalysisService
from backend.advisory_service import AdvisoryService
from backend.scheduler import init_scheduler

# Initialize services
data_service = DataService()
analysis_service = AnalysisService()
advisory_service = AdvisoryService()

# Initialize scheduler
scheduler = None

# ============================================================
# HEALTH CHECK ENDPOINT
# ============================================================

@app.get("/health")
async def health_check():
    """Check if API is running"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# ============================================================
# DATA INGESTION ENDPOINTS (Rune α)
# ============================================================

@app.get("/api/v1/companies/{ticker}")
async def fetch_company(ticker: str):
    """Fetch company data for a ticker"""
    try:
        company_data = data_service.fetch_company_data(ticker)
        return {
            "success": True,
            "data": company_data,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/analyze")
async def analyze_companies(ticker_list: TickerList):
    tickers = ticker_list.tickers
    """Fetch data for multiple companies"""
    try:
        companies_data = []
        for ticker in tickers:
            data = data_service.fetch_company_data(ticker)
            companies_data.append(data)
        
        return {
            "success": True,
            "data": companies_data,
            "count": len(companies_data),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================
# ANALYSIS ENDPOINTS (Rune β)
# ============================================================

@app.post("/api/v1/analyze")
async def analyze_companies(tickers: list):
    """Analyze companies and return scores"""
    try:
        companies_data = []
        for ticker in tickers:
            data = data_service.fetch_company_data(ticker)
            companies_data.append(data)
        
        analysis = analysis_service.analyze_companies(companies_data)
        
        return {
            "success": True,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================
# ADVISORY ENDPOINTS (Rune γ)
# ============================================================

@app.post("/api/v1/advise")
async def generate_advice(tickers: list):
    """Generate investment advice"""
    try:
        companies_data = []
        for ticker in tickers:
            data = data_service.fetch_company_data(ticker)
            companies_data.append(data)
        
        analysis = analysis_service.analyze_companies(companies_data)
        advice = advisory_service.generate_advice(analysis)
        
        return {
            "success": True,
            "advice": advice,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================
# META-SYNTHESIS ENDPOINT
# ============================================================

@app.post("/api/v1/wealth-advisor")
async def complete_wealth_advisory(
    tickers: list,
    portfolio: dict = None,
    background_tasks: BackgroundTasks = None
):
    """Complete wealth advisory workflow"""
    try:
        # Step 1: Fetch data
        companies_data = []
        for ticker in tickers:
            data = data_service.fetch_company_data(ticker)
            companies_data.append(data)
        
        # Step 2: Analyze
        analysis = analysis_service.analyze_companies(companies_data)
        
        # Step 3: Generate advice
        advice = advisory_service.generate_advice(analysis)
        
        # Step 4: Generate final advisory
        final_advisory = {
            "timestamp": datetime.now().isoformat(),
            "companies_analyzed": len(tickers),
            "top_recommendations": analysis[:3],
            "advisory_summary": advice,
            "portfolio_suggestions": {
                "aggressive": "70% high potential, 25% medium, 5% low",
                "balanced": "50% high potential, 40% medium, 10% low",
                "conservative": "30% high potential, 50% medium, 20% low"
            }
        }
        
        return {
            "success": True,
            "advisory": final_advisory
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================
# STARTUP EVENT
# ============================================================

@app.on_event("startup")
async def startup_event():
    """Initialize scheduler on app startup"""
    global scheduler
    scheduler = init_scheduler()
    print("✓ Application started with scheduler")

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown scheduler"""
    if scheduler:
        scheduler.shutdown()
        print("✓ Scheduler shut down")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", False)
    )


