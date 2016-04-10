from . import settings

if settings.DEBUG:
    from mmc.mixins import inject_management

    inject_management()
