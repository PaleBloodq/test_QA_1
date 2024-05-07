from aiogram import F, types, Dispatcher
from aiogram.filters import Command, BaseFilter



class IsReplyFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return message.reply_to_message is not None


def register_routes(dp: Dispatcher):
    from app import windows
    dp.message.register(windows.start, Command('start'))
    dp.message.register(windows.answer_order, IsReplyFilter())
    dp.callback_query.register(windows.show_id, F.data.regexp(r'order_show_.*'))
