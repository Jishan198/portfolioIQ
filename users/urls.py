from django.urls import path
from .views import register_view, login_view, logout_view
# ... (keep your existing JWT imports)

urlpatterns = [
    # ... (keep your existing JWT paths)
    
    # Web Auth Paths
    path('login/', login_view, name='login_view'),
    path('register/', register_view, name='register_view'),
    path('logout/', logout_view, name='logout_view'),
]