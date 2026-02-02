from django.urls import path
from .views import DashboardView, CreateShortURLView, RedirectURLView, DeleteShortURLView, UpdateShortURLView, QRCodeView, QRPreviewView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('create/', CreateShortURLView.as_view(), name='create'),
    path('edit/<int:pk>/', UpdateShortURLView.as_view(), name='edit'),
    path('delete/<int:pk>/', DeleteShortURLView.as_view(), name='delete'),
    path('r/<str:key>/', RedirectURLView.as_view(), name='redirect'),
    path('qr/<int:pk>/', QRCodeView.as_view(), name='qr'),
    path('qr-preview/<int:pk>/', QRPreviewView.as_view(), name='qr_preview'),
]