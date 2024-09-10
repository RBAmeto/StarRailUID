import re

from gsuid_core.bot import Bot
from gsuid_core.models import Event
from gsuid_core.sv import SV
from gsuid_core.utils.database.api import get_uid
from gsuid_core.utils.database.models import GsBind
from gsuid_core.utils.error_reply import UID_HINT

from .draw_abyss_card import draw_abyss_img
from ..utils.sr_prefix import PREFIX

sv_abyss_boss = SV("sr查询末日幻影")


@sv_abyss_boss.on_command(
    (
        f"{PREFIX}查询末日幻影",
        f"{PREFIX}查询上期末日幻影",
        f"{PREFIX}上期末日",
        f"{PREFIX}末日",
    ),
    block=True,
)
async def send_srabyss_info(bot: Bot, ev: Event):
    name = "".join(re.findall("[\u4e00-\u9fa5]", ev.text))
    if name:
        return None

    await bot.logger.info("开始执行[sr查询末日幻影信息]")
    uid, user_id = await get_uid(bot, ev, GsBind, "sr", True)
    if uid is None:
        return await bot.send(UID_HINT)
    await bot.logger.info(f"[sr查询末日幻影信息]uid: {uid}")

    if "上期" in ev.command:
        schedule_type = "2"
    else:
        schedule_type = "1"
    await bot.logger.info(f"[sr查询末日幻影信息]末日幻影期数: {schedule_type}")

    im = await draw_abyss_img(user_id, uid, ev.sender, schedule_type)
    await bot.send(im)
    return None