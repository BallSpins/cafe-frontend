import json
import os
from datetime import datetime, timedelta
from kivy.app import App


def get_token_path(filename: str = 'token.json') -> str:
    """
    Returns a cross-platform-safe path to store the token file.
    """
    app = App.get_running_app()
    data_dir = app.user_data_dir if app else os.getcwd()
    full_path = os.path.join(data_dir, filename)
    print(f"[DEBUG] Token path: {full_path}")
    return os.path.join(data_dir, filename)


def save_token(token: str) -> None:
    data = {
        'token': token,
        'created_at': datetime.utcnow().isoformat()
    }
    path = get_token_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'w') as file:
        json.dump(data, file)
    print(f'Token saved to {path}')


def load_token() -> tuple[str, str]:
    path = get_token_path()
    try:
        with open(path, 'r') as file:
            data = json.load(file)
            token = data.get('token', '')
            created_at = data.get('created_at', '')
            print(f'Token loaded: {token}, created at: {created_at}')
            return token, created_at
    except FileNotFoundError:
        print(f'File {path} not found.')
        return '', ''


def check_expired_token(created_at: str, days: int = 2) -> bool:
    try:
        token_time = datetime.fromisoformat(created_at)
        expired = datetime.utcnow() - token_time > timedelta(days=days)
        print(f'Token age: {(datetime.utcnow() - token_time).days} day(s). Expired: {expired}')
        return expired
    except Exception as e:
        print(f'Error checking expiration: {e}')
        return True  # Treat invalid time as expired
    
def delete_token() -> None:
    path = get_token_path()
    try:
        os.remove(path)
        print(f'Token deleted: {path}')
    except FileNotFoundError:
        print(f'No token file to delete at: {path}')
    except Exception as e:
        print(f'Error deleting token: {e}')