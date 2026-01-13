from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    TG_BOT_TOKEN: str
    TG_CHAT_ID: str
    
    # 默认值参考用户示例，但建议通过 .env 覆盖
    BUY_PRICE: float = 4550.0
    SELL_PRICE: float = 4750.0
    
    # API URL
    GOLD_API_URL: str = "https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT"

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
