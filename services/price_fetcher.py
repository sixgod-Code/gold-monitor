import requests
import logging
from config import settings
import pandas as pd

logger = logging.getLogger(__name__)

def get_gold_price() -> float:
    """
    获取实时金价 (以 PAXG/USDT 为锚定)
    """
    try:
        url = settings.GOLD_API_URL
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        price = float(data['pax-gold']['usd'])
        logger.info(f"Fetched price: {price}")
        return price
    except requests.RequestException as e:
        logger.error(f"Failed to fetch gold price: {e}")
        raise
    except (KeyError, ValueError) as e:
        logger.error(f"Failed to parse price data: {e}")
        raise ValueError(f"Invalid API response: {e}")

def get_gold_rsi() -> float:
    """
    计算黄金的 RSI 指标
    """
    try:
        url = settings.GOLD_HISTORY_API_URL
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        prices = [p[1] for p in data['prices']]
        
        if len(prices) < settings.RSI_PERIOD:
            logger.warning("Not enough data to calculate RSI")
            return 50.0  # 返回中性值
            
        df = pd.DataFrame(prices, columns=['price'])
        delta = df['price'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=settings.RSI_PERIOD).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=settings.RSI_PERIOD).mean()
        
        # 避免除以零
        loss = loss.replace(0, 0.000001)
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        current_rsi = float(rsi.iloc[-1])
        logger.info(f"Calculated RSI: {current_rsi}")
        return current_rsi
    except Exception as e:
        logger.error(f"Failed to calculate RSI: {e}")
        return 50.0  # 发生错误时返回中性值
