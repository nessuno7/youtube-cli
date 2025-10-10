from platformdirs import user_data_dir
from pathlib import Path

APP_NAME = "ytcli"
APP_AUTHOR = "nessuno7" 

# Base directory for app data
data_dir = Path(user_data_dir(APP_NAME, APP_AUTHOR))
clips_dir = data_dir / "clips"
videos_dir = data_dir / "videos"
config_path = data_dir / "config.json"
database_dir = data_dir / "databases"
channel_database = data_dir / "channels.db"

# Ensure folders exist
def config_function():
    for path in [data_dir, clips_dir, videos_dir, database_dir]:
        path.mkdir(parents=True, exist_ok=True)
