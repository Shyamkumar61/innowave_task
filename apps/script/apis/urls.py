from django.urls import path
from apps.script.apis.views import ScriptView, ScriptDetailView


urlpatterns = [
    path('scripts/', ScriptView.as_view(), name='scripts'),
    path('scripts-detail/<int:pk>/', ScriptDetailView.as_view(), name='script-detail')
]
