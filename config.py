# config.py

import os
from pathlib import Path

base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'data', 'carl_database.db')
backup_path=os.path.join(base_dir, 'data','old_tables')

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_path
    SECRET_KEY = 'AAAAAAAAAAA'


PROJECT_ROOT = Path(__file__).parent
AUDIO_OUTPUT = PROJECT_ROOT / "audio" / "generated_audio"