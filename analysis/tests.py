from celery import shared_task
from .models import StockAnalysis
from .services import generate_risk_analysis, generate_vision_analysis


@shared_task
def analyze_stock_task(analysis_id, ticker, current_price, company_name):
    analysis = StockAnalysis.objects.get(id=analysis_id)
    try:
        report = generate_risk_analysis(ticker, current_price, company_name)
        if not report:
            analysis.status = 'FAILED'
            analysis.ai_report = '{"error": "Gemini returned no response. You may have hit the free tier rate limit. Wait 1 minute and try again."}'
        else:
            analysis.ai_report = report
            analysis.status = 'COMPLETED'
        analysis.save()
        return f"Done: {ticker}"
    except Exception as e:
        analysis.status = 'FAILED'
        analysis.ai_report = f'{{"error": "{str(e)}"}}'
        analysis.save()
        return f"Failed: {str(e)}"


@shared_task
def analyze_screenshot_task(analysis_id, base64_image, mime_type):
    analysis = StockAnalysis.objects.get(id=analysis_id)
    try:
        report = generate_vision_analysis(base64_image, mime_type)
        if not report:
            analysis.status = 'FAILED'
            analysis.ai_report = '{"error": "Gemini returned no response. You may have hit the free tier rate limit. Wait 1 minute and try again."}'
        else:
            analysis.ai_report = report
            analysis.status = 'COMPLETED'
        analysis.save()
        return "Done: Screenshot analyzed."
    except Exception as e:
        analysis.status = 'FAILED'
        analysis.ai_report = f'{{"error": "{str(e)}"}}'
        analysis.save()
        return f"Failed: {str(e)}"

# Create your tests here.
