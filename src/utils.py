import os
import json
import requests
from datetime import datetime, timedelta
from kivy.app import App

class CartItem():
    def __init__(self, menu_id: int, quantity: int = 1):
        self.menu_id = menu_id
        self.quantity = quantity

cart_items: list[CartItem] = []

def get_cart_count_id(menu_id: int):
    for item in cart_items:
        if item.menu_id == menu_id:
            return item.quantity
    return 0

def get_cart_items() -> list[CartItem]:
    return cart_items

def add_cart_items(menu_id: int) -> None:
    for item in cart_items:
        if item.menu_id == menu_id:
            item.quantity += 1
            return
    cart_items.append(CartItem(menu_id, 1))

def clear_cart_items():
    cart_items.clear()

def delete_cart_items(menu_id: int) -> None:
    for item in cart_items:
        if item.menu_id == menu_id:
            item.quantity -= 1
            if item.quantity <= 0:
                cart_items.remove(item)
            return

def post_order():
    url = 'https://cafe.ddns.net/pesanan/'
    _, _, user_id = load_token()

    if user_id == -1 or not cart_items:
        print("Tidak ada user_id atau cart kosong.")
        # return None
    
    menu_ids = []
    for item in cart_items:
        menu_ids.extend([item.menu_id] * item.quantity)

    data = {
        'user_id': user_id,
        'menu_ids': menu_ids,
        'status': 'pending'
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        print("Pesanan berhasil dibuat:", response.json())
        clear_cart_items()
        # return response.json()
    except requests.exceptions.RequestException as e:
        print("Gagal mengirim pesanan:", e)
        # return None

def get_token_path(filename: str = 'token.json') -> str:
    """
    Returns a cross-platform-safe path to store the token file.
    """
    app = App.get_running_app()
    data_dir = app.user_data_dir if app else os.getcwd()
    full_path = os.path.join(data_dir, filename)
    print(f"[DEBUG] Token path: {full_path}")
    return os.path.join(data_dir, filename)


def save_token(token: str, user_id: int) -> None:
    data = {
        'token': token,
        'user_id': user_id,
        'created_at': datetime.utcnow().isoformat()
    }
    path = get_token_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'w') as file:
        json.dump(data, file)
    print(f'Token saved to {path}')


def load_token() -> tuple[str, str, int]:
    path = get_token_path()
    try:
        with open(path, 'r') as file:
            data = json.load(file)
            token = data.get('token', '')
            user_id = data.get('user_id', -1)
            created_at = data.get('created_at', '')
            print(f'Token loaded: {token}, user_id: {user_id}, created at: {created_at}')
            return token, created_at, user_id
    except FileNotFoundError:
        print(f'File {path} not found.')
        return '', '', -1


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