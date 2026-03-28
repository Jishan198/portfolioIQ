"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from portfolios.views import main_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # The Frontend Web Dashboard (Root URL)
    path('', main_dashboard, name='main_dashboard'),
    
    # Your REST API Endpoints
    path('api/v1/auth/', include('users.urls')),
    path('api/v1/', include('portfolios.urls')),
    path('api/v1/', include('analysis.urls')),
]
