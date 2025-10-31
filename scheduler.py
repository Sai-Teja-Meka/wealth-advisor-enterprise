# ============================================================
# SCHEDULER FOR AUTOMATIC UPDATES
# ============================================================

from apscheduler.schedulers.background import BackgroundScheduler
from backend.data_service import DataService
from backend.analysis_service import AnalysisService
from backend.advisory_service import AdvisoryService
from datetime import datetime
import json

def init_scheduler():
    """Initialize background scheduler"""
    
    scheduler = BackgroundScheduler()
    
    data_service = DataService()
    analysis_service = AnalysisService()
    advisory_service = AdvisoryService()
    
    def hourly_wealth_advisor():
        """Run wealth advisor every hour"""
        print(f"\n{'='*70}")
        print(f"SCHEDULED WEALTH ADVISOR - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}")
        
        try:
            tickers = ["AAPL", "MSFT", "GOOGL", "NVDA", "SHOP", "UPST"]
            
            # Fetch data
            companies = []
            for ticker in tickers:
                data = data_service.fetch_company_data(ticker)
                if data:
                    companies.append(data)
            
            # Analyze
            analysis = analysis_service.analyze_companies(companies)
            
            # Generate advice
            advice = advisory_service.generate_advice(analysis)
            
            print(f"✓ Advisory generated for {len(companies)} companies")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Add hourly job
    scheduler.add_job(
        hourly_wealth_advisor,
        'interval',
        hours=1,
        id='wealth_advisor_hourly',
        name='Hourly wealth advisor update'
    )
    
    return scheduler
