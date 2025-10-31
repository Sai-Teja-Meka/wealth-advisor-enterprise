# ============================================================
# ADVISORY SERVICE (Rune γ)
# ============================================================

import os
from langchain_groq import ChatGroq
import json

class AdvisoryService:
    """Generates investment advice using AI"""
    
    def __init__(self):
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.3-70b-versatile",
            temperature=0.2
        )
    
    def generate_advice(self, analysis_results: list) -> str:
        """Generate investment advice"""
        
        top_5 = analysis_results[:5]
        
        prompt = f"""
You are a professional investment advisor. Based on these analysis results,
provide 3-4 sentence investment advice:

TOP OPPORTUNITIES:
{json.dumps(top_5, indent=2, default=str)}

Provide advice that:
1. Identifies the best investment opportunity
2. Notes any risks
3. Suggests diversification
4. Explains why for small company investors

Keep it practical and concise.
"""
        
        response = self.llm.invoke(prompt)
        return response.content
