from django.db import models

class Report(models.Model):
    task_id = models.CharField(max_length=255, unique=True)
    student_id = models.CharField(max_length=255)
    html_content = models.TextField(null=True, blank=True)
    pdf_file = models.BinaryField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)