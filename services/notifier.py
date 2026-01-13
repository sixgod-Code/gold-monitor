import requests
import logging
from config import settings

logger = logging.getLogger(__name__)

def send_tg_msg(text: str) -> None:
    """
    发送消息到 Telegram Bot
    
    Args:
        text: 消息内容
    """
    if not settings.TG_BOT_TOKEN or not settings.TG_CHAT_ID:
        logger.warning("Telegram configuration missing, skipping notification.")
        return

    try:
        url = f"https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": settings.TG_CHAT_ID,
            "text": text,
            "parse_mode": "HTML"
        }
        
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        logger.info("Notification sent successfully.")
        
    except requests.RequestException as e:
        logger.error(f"Failed to send Telegram message: {e}")
