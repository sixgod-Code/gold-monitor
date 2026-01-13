import logging
import sys
from config import settings
from services.price_fetcher import get_gold_price, get_gold_rsi
from services.notifier import send_tg_msg

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Gold Price Monitor with RSI logic...")
    
    try:
        # 获取价格和 RSI
        current_price = get_gold_price()
        current_rsi = get_gold_rsi()
        
        logger.info(f"Price: ${current_price:.2f} | RSI: {current_rsi:.2f}")
        
        message = ""
        
        # 买入建议：价格低于阈值且 RSI 处于超卖区 (< 30)
        if current_price <= settings.BUY_PRICE and current_rsi <= settings.RSI_BUY_THRESHOLD:
            message = (
                f"🔔 <b>黄金买入强烈建议！</b>\n\n"
                f"当前价格: ${current_price:.2f}\n"
                f"当前 RSI: {current_rsi:.2f} (超卖)\n"
                f"逻辑：价格已低于 ${settings.BUY_PRICE:.2f} 且技术指标显示超卖，是较好的左侧建仓机会。"
            )
            logger.info("Strong buy signal triggered.")
            
        # 卖出建议：价格高于阈值且 RSI 处于超买区 (> 70)
        elif current_price >= settings.SELL_PRICE and current_rsi >= settings.RSI_SELL_THRESHOLD:
            message = (
                f"🚀 <b>黄金止盈强烈建议！</b>\n\n"
                f"当前价格: ${current_price:.2f}\n"
                f"当前 RSI: {current_rsi:.2f} (超买)\n"
                f"逻辑：价格已超过 ${settings.SELL_PRICE:.2f} 且技术指标显示超买，建议注意风险或获利了结。"
            )
            logger.info("Strong sell signal triggered.")
            
        # 弱买入建议：仅价格达标
        elif current_price <= settings.BUY_PRICE:
            message = (
                f"⚠️ <b>黄金价格达到买入线 (RSI 尚未超卖)</b>\n\n"
                f"当前价格: ${current_price:.2f}\n"
                f"当前 RSI: {current_rsi:.2f}\n"
                f"逻辑：价格虽然达标，但 RSI 还在中性区间，建议谨慎分批买入。"
            )
            logger.info("Price buy threshold reached, but RSI neutral.")

        if message:
            send_tg_msg(message)
            logger.info("Notification sent.")
            
    except Exception as e:
        logger.error(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()
