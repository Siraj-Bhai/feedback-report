## Setup Instructions

```bash
git clone <repo-url>
cd feedback_report
poetry install
docker-compose -f docker/docker-compose.yml up --build
```

Access API at `http://localhost:8000`
Monitor tasks at `http://localhost:5555`

## API
- `POST /assignment/html`: Generate HTML report
- `GET /assignment/html/<task_id>`: Get HTML or status
- `POST /assignment/pdf`: Generate PDF report
- `GET /assignment/pdf/<task_id>`: Get PDF or status
