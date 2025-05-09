from celery import shared_task
from .models import Report
from io import BytesIO
from reportlab.pdfgen import canvas

@shared_task(bind=True)
def generate_html_report(self, data):
    try:
        student_id = data[0]['student_id']
        events = data[0]['events']
        sorted_units = sorted(set(e['unit'] for e in events))
        alias_map = {unit: f"Q{idx+1}" for idx, unit in enumerate(sorted_units)}
        event_order = ' -> '.join([alias_map[e['unit']] for e in events])
        html = f"<h2>Student ID: {student_id}</h2><p>Event Order: {event_order}</p>"

        Report.objects.create(task_id=self.request.id, student_id=student_id, html_content=html)
        return {'status': 'completed'}
    except Exception as e:
        raise self.retry(exc=e, countdown=5, max_retries=3)

@shared_task(bind=True)
def generate_pdf_report(self, data):
    try:
        student_id = data[0]['student_id']
        events = data[0]['events']
        sorted_units = sorted(set(e['unit'] for e in events))
        alias_map = {unit: f"Q{idx+1}" for idx, unit in enumerate(sorted_units)}
        event_order = ' -> '.join([alias_map[e['unit']] for e in events])

        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 800, f"Student ID: {student_id}")
        p.drawString(100, 780, f"Event Order: {event_order}")
        p.save()

        pdf_data = buffer.getvalue()
        buffer.close()

        Report.objects.create(task_id=self.request.id, student_id=student_id, pdf_file=pdf_data)
        return {'status': 'completed'}
    except Exception as e:
        raise self.retry(exc=e, countdown=5, max_retries=3)