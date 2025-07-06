import discord
import asyncio
import logging
from typing import Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

# Khởi tạo client Discord
client = discord.Client(intents=discord.Intents.default())
is_ready = asyncio.Event()

@client.event
async def on_ready():
    """Được gọi khi client Discord đã sẵn sàng."""
    logger.info(f"Discord bot đã đăng nhập thành công dưới tên {client.user}")
    is_ready.set()

async def send_discord_notification(message: str, channel_id: Optional[int] = None) -> bool:
    """
    Gửi thông báo đến kênh Discord được chỉ định.
    
    Args:
        message: Nội dung tin nhắn cần gửi
        channel_id: ID kênh Discord (nếu không cung cấp, sẽ sử dụng kênh mặc định từ cấu hình)
    
    Returns:
        bool: True nếu gửi thành công, False nếu thất bại
    """
    if not settings.DISCORD_BOT_TOKEN or not (channel_id or settings.DISCORD_NOTIFICATION_CHANNEL_ID):
        logger.warning("Thiếu cấu hình Discord. Không thể gửi thông báo.")
        return False
    
    target_channel_id = channel_id or settings.DISCORD_NOTIFICATION_CHANNEL_ID
    
    try:
        # Khởi động client nếu chưa đăng nhập
        if not client.is_ready():
            # Chạy client trong một task riêng biệt
            asyncio.create_task(client.start(settings.DISCORD_BOT_TOKEN))
            # Đợi cho đến khi client sẵn sàng, tối đa 10 giây
            await asyncio.wait_for(is_ready.wait(), timeout=10.0)
        
        # Lấy kênh và gửi tin nhắn
        channel = client.get_channel(target_channel_id)
        if not channel:
            logger.error(f"Không tìm thấy kênh Discord với ID {target_channel_id}")
            return False
        
        await channel.send(message)
        return True
    
    except asyncio.TimeoutError:
        logger.error("Hết thời gian chờ kết nối đến Discord")
        return False
    except discord.LoginFailure:
        logger.error("Token Discord không hợp lệ")
        return False
    except Exception as e:
        logger.error(f"Lỗi khi gửi thông báo Discord: {str(e)}")
        return False 