from aiogram import Router


def setup_routers() -> Router:
    from . import start, toggle

    router = Router()

    router.include_routers(start.router, toggle.router)

    return router
