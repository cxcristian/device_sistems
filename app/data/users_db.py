users_db: list[dict] = [
    {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "admin", "is_active": True},
    {"id": 2, "name": "Bob", "email": "bob@example.com", "role": "user", "is_active": True},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com", "role": "support", "is_active": False},
    {"id": 4, "name": "Diana", "email": "diana@example.com", "role": "user", "is_active": True},
    {"id": 5, "name": "Eve", "email": "eve@example.com", "role": "admin", "is_active": False},
]
_id_counter: int = 6
def get_next_id() -> int:
    global _id_counter
    nid = _id_counter
    _id_counter += 1
    return nid