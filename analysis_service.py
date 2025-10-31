# ============================================================
# ANALYSIS SERVICE (Rune β)
# ============================================================

class AnalysisService:
    """Analyzes companies and generates scores"""
    
    def calculate_score(self, company: dict) -> float:
        """Calculate investment score 0-100"""
        score = 0
        
        # PE Ratio
        if 15 <= company.get("pe_ratio", 20) <= 25:
            score += 25
        elif company.get("pe_ratio", 20) < 50:
            score += 15
        else:
            score += 5
        
        # Profit Margin
        profit_margin = company.get("profit_margin", 0.15)
        if profit_margin > 0.20:
            score += 20
        elif profit_margin > 0.10:
            score += 15
        else:
            score += 5
        
        # ROE
        roe = company.get("roe", 0.15)
        if roe > 0.15:
            score += 20
        elif roe > 0.10:
            score += 15
        else:
            score += 5
        
        # Debt/Equity
        debt_equity = company.get("debt_equity", 1.0)
        if debt_equity < 1.0:
            score += 15
        elif debt_equity < 2.0:
            score += 10
        else:
            score += 5
        
        # Current Ratio
        current_ratio = company.get("current_ratio", 2.0)
        if 1.5 <= current_ratio <= 3.0:
            score += 10
        elif current_ratio > 1.0:
            score += 5
        else:
            score += 2
        
        # Revenue Growth
        revenue_growth = company.get("revenue_growth", 0.10)
        if revenue_growth > 0.15:
            score += 10
        elif revenue_growth > 0.05:
            score += 5
        else:
            score += 2
        
        return min(score, 100)
    
    def get_recommendation(self, score: float, debt_equity: float, current_ratio: float) -> tuple:
        """Get recommendation and risk level"""
        if debt_equity > 3.0 or current_ratio < 1.0:
            risk = "HIGH"
        elif debt_equity > 2.0 or current_ratio < 1.5:
            risk = "MEDIUM"
        else:
            risk = "LOW"
        
        if score >= 80 and risk == "LOW":
            return "STRONG BUY", risk
        elif score >= 70:
            return "BUY", risk
        elif score >= 50:
            return "HOLD", risk
        elif score >= 30:
            return "WEAK SELL", risk
        else:
            return "SELL", risk
    
    def analyze_companies(self, companies: list) -> list:
        """Analyze all companies"""
        results = []
        
        for company in companies:
            if not company:
                continue
            
            score = self.calculate_score(company)
            recommendation, risk = self.get_recommendation(
                score,
                company.get("debt_equity", 1.0),
                company.get("current_ratio", 2.0)
            )
            
            results.append({
                "ticker": company["ticker"],
                "name": company.get("name", "N/A"),
                "price": company.get("price", 0),
                "score": round(score, 1),
                "recommendation": recommendation,
                "risk": risk,
                "metrics": {
                    "pe": f"{company.get('pe_ratio', 0):.1f}x",
                    "profit_margin": f"{company.get('profit_margin', 0)*100:.1f}%",
                    "roe": f"{company.get('roe', 0)*100:.1f}%",
                    "debt_equity": f"{company.get('debt_equity', 0):.2f}",
                    "current_ratio": f"{company.get('current_ratio', 0):.2f}"
                }
            })
        
        # Sort by score
        results.sort(key=lambda x: x["score"], reverse=True)
        return results
