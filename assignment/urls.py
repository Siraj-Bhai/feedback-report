from django.urls import path
from .views import GenerateHTMLReport, GetHTMLReport, GeneratePDFReport, GetPDFReport

urlpatterns = [
    path('html/', GenerateHTMLReport.as_view()),
    path('html/<str:task_id>/', GetHTMLReport.as_view()),
    path('pdf/', GeneratePDFReport.as_view()),
    path('pdf/<str:task_id>/', GetPDFReport.as_view()),
]