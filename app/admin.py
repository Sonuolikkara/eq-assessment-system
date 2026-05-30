# 1. Navigate to project
cd C:\Users\sabuv\eq_system

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies (will download ~260 MB for ML model on first run)
pip install -r requirements.txt

# 4. Run database migrations
python manage.py migrate

# 5. Start the server
python manage.py runserverfrom django.contrib import admin
from .models import Assessment

admin.site.register(Assessment)
