from django.db import models
from django.conf import settings

class StockAnalysis(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='analyses')
    ticker = models.CharField(max_length=20)
    ai_report = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='PENDING') # PENDING, COMPLETED, FAILED
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticker} Analysis for {self.user.email} ({self.status})"

# Create your models here.
