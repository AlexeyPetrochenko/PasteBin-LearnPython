from app_paste_bin.models import db
from app_paste_bin.app import create_app

app = create_app()
with app.app_context():
    db.create_all()