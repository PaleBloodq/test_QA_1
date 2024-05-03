from .dialogs import DLGS


def register_dialogs(dp):
    for DLG in DLGS:
        dp.include_router(DLG)
