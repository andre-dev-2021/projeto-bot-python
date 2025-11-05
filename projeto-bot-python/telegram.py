import requests as rq
import os
from dotenv import load_dotenv

load_dotenv(".env")

BASE_URL = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}"

def get_updates(offset: int = None, timeout: int = 60) -> tuple:
    """get_updates(offset, timeout)

    Retorna dados da ultima mensagem recebida pelo chatbot.

    Args:
        offset (int, optional): None por padrão
        timeout (int, optional): 60 por padrão

    Returns:
        tuple: id, texto da mensagem, id do update e tipo da mensagem (texto ou comando do bot).
    """

    params = {"timeout": timeout}
    if offset is not None:
        params["offset"] = offset

    try:
        res = rq.get(f"{BASE_URL}/getUpdates", params=params, timeout=timeout + 5)
        res = res.json()
    except Exception:
        return None, None, None

    results = res.get("result", [])
    if not results:
        return None, None, None

    last_update = results[-1]
    update_id = last_update.get("update_id")
    message = last_update.get("message", {})
    msg_type = message.get("entities", [{"type": "text"}])[0]["type"]
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text")
    return chat_id, text, update_id,msg_type


def send_message(chat_id:int, text:str):
    """send_message(chat_id, text) -> None

    Envia mensagem para o usuário.

    Args:
        chat_id (int): Id do chat
        text (str): Texto que será enviado.

    Returns:
        None
    """
    try:
        return rq.post(
            url=f"{BASE_URL}/sendMessage",
            data={
                "chat_id": chat_id,
                "text": text,
            },
            timeout=10,
        ).json()
    except Exception:
        return None