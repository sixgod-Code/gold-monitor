import requests
import logging
from config import settings

logger = logging.getLogger(__name__)

def get_gold_price() -> float:
    """
    获取实时金价 (以 PAXG/USDT 为锚定)
    
    Returns:
        float: 当前最新价格
        
    Raises:
        requests.RequestException: 网络请求失败
        ValueError: 数据解析失败
    """
    try:
        url = settings.GOLD_API_URL
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        # CoinGecko format: {'pax-gold': {'usd': 2000.0}}
        price = float(data['pax-gold']['usd'])
        logger.info(f"Fetched price: {price}")
        return price
        
    except requests.RequestException as e:
        logger.error(f"Failed to fetch gold price: {e}")
        raise
    except (KeyError, ValueError) as e:
        logger.error(f"Failed to parse price data: {e}")
        raise ValueError(f"Invalid API response: {e}")
