from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult
from .tasks import generate_html_report, generate_pdf_report
from .models import Report

class GenerateHTMLReport(APIView):
    def post(self, request):
        task = generate_html_report.delay(request.data)
        return Response({'task_id': task.id}, status=status.HTTP_202_ACCEPTED)

class GetHTMLReport(APIView):
    def get(self, request, task_id):
        result = AsyncResult(task_id)
        if result.state == 'PENDING':
            return Response({'status': 'pending'})
        elif result.state == 'FAILURE':
            return Response({'status': 'failed'})
        elif result.state == 'SUCCESS':
            try:
                report = Report.objects.get(task_id=task_id)
                return Response({'status': 'completed', 'html': report.html_content})
            except Report.DoesNotExist:
                return Response({'status': 'not_found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'status': result.state})

class GeneratePDFReport(APIView):
    def post(self, request):
        task = generate_pdf_report.delay(request.data)
        return Response({'task_id': task.id}, status=status.HTTP_202_ACCEPTED)

class GetPDFReport(APIView):
    def get(self, request, task_id):
        result = AsyncResult(task_id)
        if result.state == 'PENDING':
            return Response({'status': 'pending'})
        elif result.state == 'FAILURE':
            return Response({'status': 'failed'})
        elif result.state == 'SUCCESS':
            try:
                report = Report.objects.get(task_id=task_id)
                return Response(report.pdf_file, content_type='application/pdf')
            except Report.DoesNotExist:
                return Response({'status': 'not_found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'status': result.state})