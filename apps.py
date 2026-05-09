from django.apps import AppConfig


class OnlineMarketplaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Online_Marketplace'

    def ready(self):
        import Online_Marketplace.signals