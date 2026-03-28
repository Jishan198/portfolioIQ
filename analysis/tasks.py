from celery import shared_task
from .models import StockAnalysis
from .services import generate_risk_analysis

@shared_task
def analyze_stock_task(analysis_id, ticker, current_price, company_name):
    try:
        # Fetch the pending record
        analysis = StockAnalysis.objects.get(id=analysis_id)
        
        # Call the Gemini AI Engine
        report = generate_risk_analysis(ticker, current_price, company_name)
        
        # Update and save the record
        analysis.ai_report = report
        analysis.status = 'COMPLETED'
        analysis.save()
        
        return f"Success: Analysis completed for {ticker}"
    except Exception as e:
        analysis = StockAnalysis.objects.get(id=analysis_id)
        analysis.status = 'FAILED'
        analysis.save()
        return f"Failed: {str(e)}"
    
from .services import generate_vision_analysis

@shared_task
def analyze_screenshot_task(analysis_id, base64_image, mime_type):
    try:
        analysis = StockAnalysis.objects.get(id=analysis_id)
        report = generate_vision_analysis(base64_image, mime_type)
        
        analysis.ai_report = report
        analysis.status = 'COMPLETED'
        analysis.save()
        return "Success: Screenshot analyzed."
    except Exception as e:
        analysis = StockAnalysis.objects.get(id=analysis_id)
        analysis.status = 'FAILED'
        analysis.save()
        return f"Failed: {str(e)}"