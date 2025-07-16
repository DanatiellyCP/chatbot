from django.urls import path
from whatsapp import views

urlpatterns = [
    path("webhook/", views.webhook_whatsapp, name="webhook"),
    path("painel_chat/", views.painel_chat, name="painel_chat"),
]
