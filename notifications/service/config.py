def tg_token_unspecified():
    print("Telegram token unspecified")
    return "Telegram token unspecified"

def tg_user_ids_unspecified():
    print("Telegram ids unspecified")
    return ["Telegram token unspecified"]

config = {
    "secret_token": "my_super_secret_notifications_token",
    "flask_port" : 5555,
    "socket_port": 5556,
    "tg_token": tg_token_unspecified(),
    "tg_user_ids": tg_user_ids_unspecified(),
    "tg_enabled": False
}