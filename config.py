from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    TG_BOT_TOKEN: str
    TG_CHAT_ID: str

    # 默认值参考用户示例，但建议通过 .env 覆盖
    BUY_PRICE: float = 4550.0
    SELL_PRICE: float = 4750.0
    
    # RSI 相关设置
    RSI_PERIOD: int = 14
    RSI_BUY_THRESHOLD: float = 30.0
    RSI_SELL_THRESHOLD: float = 70.0

    # API URL
    # 使用 CoinGecko API (无需 Key, 限制较少)
    GOLD_API_URL: str = "https://api.coingecko.com/api/v3/simple/price?ids=pax-gold&vs_currencies=usd"
    # 获取历史数据以计算 RSI (使用 CoinGecko)
    GOLD_HISTORY_API_URL: str = "https://api.coingecko.com/api/v3/coins/pax-gold/market_chart?vs_currency=usd&days=30"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
