Testing the Fix
Step 1: Run your Flask app
bash
python run.py
Step 2: Start Celery worker (in a separate terminal)
bash
celery -A celery_worker.celery worker --loglevel=info
Alternative Solution: Move celery_worker.py into app/
If you prefer to keep relative imports, you can move celery_worker.py into the app/ directory:

Move file: celery_worker.py → app/celery_worker.py

Keep the relative import: from .celery_worker import celery

Update Celery worker command: celery -A app.celery_worker.celery worker --loglevel=info

Key Points to Remember
Relative imports (.module) only work within the same package

Absolute imports (module) work from the project root

Make sure to run commands from your project root directory

Ensure Redis is running before starting Celery worker

Verification Checklist
 Changed import in app/tasks.py to from celery_worker import celery

 Cleaned up celery_worker.py (removed invalid imports)

 Flask app starts without import errors

 Celery worker starts without errors

 Both can find the tasks module
