from fastapi.templating import Jinja2Templates
from pathlib import Path

TEMPLATES = Jinja2Templates(directory='templates')
MEDIA = Path('media')