import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").strip().rstrip("/")
SUPABASE_KEY = (os.environ.get("SUPABASE_KEY") or os.environ.get("SUPABASE_ANON_KEY") or "").strip()
SUPABASE_STORAGE_BUCKET = os.environ.get("SUPABASE_STORAGE_BUCKET", "lesson-videos").strip()

_client = None

def get_supabase():
    global _client
    if _client is not None:
        return _client
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    try:
        from supabase import create_client
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
        return _client
    except Exception as err:
        print(f"[Supabase Init Warning] Could not connect: {err}")
        return None

def get_supabase_video_url(relative_path: str) -> str:
    """Returns the full public Supabase storage URL for a given file path."""
    if not SUPABASE_URL or not relative_path:
        return ""
    clean_path = relative_path.lstrip("/")
    return f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_STORAGE_BUCKET}/{clean_path}"