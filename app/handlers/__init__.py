from aiogram import Router


def setup_routers() -> Router:
    from . import start, toggle, percent

    router = Router()

    router.include_routers(start.router, toggle.router, percent.router)

    return router
