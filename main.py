import logging
import sys
from config import settings
from services.price_fetcher import get_gold_price
from services.notifier import send_tg_msg

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Gold Price Monitor...")
    
    try:
        current_price = get_gold_price()
        logger.info(f"Current Gold Price (PAXG): ${current_price:.2f}")
        
        message = ""
        if current_price <= settings.BUY_PRICE:
            message = (
                f"🔔 <b>黄金买入提醒！</b>\n"
                f"当前价格: ${current_price:.2f}\n"
                f"已跌破预设值 ${settings.BUY_PRICE:.2f}，可以考虑分批建仓。"
            )
            logger.info("Price below buy threshold. Triggering notification.")
            
        elif current_price >= settings.SELL_PRICE:
            message = (
                f"🚀 <b>黄金止盈提醒！</b>\n"
                f"当前价格: ${current_price:.2f}\n"
                f"已超过预设值 ${settings.SELL_PRICE:.2f}，注意风险或考虑获利了结。"
            )
            logger.info("Price above sell threshold. Triggering notification.")
        else:
            logger.info(f"Price within range (${settings.BUY_PRICE} - ${settings.SELL_PRICE}). No action needed.")

        if message:
            send_tg_msg(message)
            
    except Exception as e:
        logger.error(f"An error occurred during execution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
