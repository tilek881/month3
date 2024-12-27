
from aiogram import Router , F

from .order import order_router
from .info_command import command_router
from .menu import menu_router
from .messages import message_router
from .review_dialog import review_router

from .start import start_router
from .admin_menu import admin_router
from .dishes import dishes_router


private_router = Router()


private_router.include_router(start_router) # ДЗ"№2
private_router.include_router(message_router)
private_router.include_router(command_router)
private_router.include_router(menu_router) # ДЗ"№2
private_router.include_router(order_router) # ДЗ"№2
private_router.include_router(review_router) # ДЗ"№3
private_router.include_router(admin_router)
private_router.include_router(dishes_router  )# ДЗ№6


private_router.message.filter(F.chat.type == 'private')
private_router.callback_query.filter(F.chat.type == 'private')