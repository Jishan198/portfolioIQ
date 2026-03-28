from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import StockAnalysis
from .tasks import analyze_stock_task, analyze_screenshot_task
import base64


@login_required(login_url='/api/v1/auth/login/')
def analysis_dashboard(request):
    return render(request, 'analysis_dashboard.html')


@login_required(login_url='/api/v1/auth/login/')
def upload_screenshot(request):
    if request.method == 'POST':
        image_file = request.FILES.get('file')

        if not image_file:
            return HttpResponse("No file uploaded.", status=400)

        image_bytes = image_file.read()
        base64_encoded = base64.b64encode(image_bytes).decode('utf-8')
        mime_type = image_file.content_type

        analysis = StockAnalysis.objects.create(user=request.user, ticker="PORTFOLIO SCREENSHOT")

        analyze_screenshot_task.delay(analysis.id, base64_encoded, mime_type)

        return render(request, 'analysis_status.html', {'analysis': analysis})

    return HttpResponse("Invalid request method.", status=405)


@login_required(login_url='/api/v1/auth/login/')
def trigger_analysis(request):
    if request.method != 'POST':
        return HttpResponse("Invalid request method.", status=405)

    ticker = request.POST.get('ticker', '').strip().upper()
    if not ticker:
        return HttpResponse("Ticker is required.", status=400)

    analysis = StockAnalysis.objects.create(user=request.user, ticker=ticker)

    analyze_stock_task.delay(analysis.id, ticker, 1000.0, "Company Name")

    return render(request, 'analysis_status.html', {'analysis': analysis})


def check_status(request, pk):
    analysis = get_object_or_404(StockAnalysis, pk=pk)
    return render(request, 'analysis_status.html', {'analysis': analysis})


@login_required(login_url='/api/v1/auth/login/')
def upload_screenshot(request):
    if request.method == 'POST':
        image_file = request.FILES.get('file')

        if not image_file:
            return HttpResponse("No file uploaded.", status=400)

        image_bytes = image_file.read()
        base64_encoded = base64.b64encode(image_bytes).decode('utf-8')
        mime_type = image_file.content_type

        analysis = StockAnalysis.objects.create(user=request.user, ticker="PORTFOLIO SCREENSHOT")

        analyze_screenshot_task.delay(analysis.id, base64_encoded, mime_type)

        return render(request, 'analysis_status.html', {'analysis': analysis})

    return HttpResponse("Invalid request method.", status=405)


@login_required(login_url='/api/v1/auth/login/')
def trigger_analysis(request):
    if request.method != 'POST':
        return HttpResponse("Invalid request method.", status=405)

    ticker = request.POST.get('ticker', '').strip().upper()
    if not ticker:
        return HttpResponse("Ticker is required.", status=400)

    analysis = StockAnalysis.objects.create(user=request.user, ticker=ticker)

    analyze_stock_task.delay(analysis.id, ticker, 1000.0, "Company Name")

    return render(request, 'analysis_status.html', {'analysis': analysis})


def check_status(request, pk):
    analysis = get_object_or_404(StockAnalysis, pk=pk)
    return render(request, 'analysis_status.html', {'analysis': analysis})