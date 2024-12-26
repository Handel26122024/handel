from django.apps import AppConfig


class EcomerceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecomerce'
    def ready(self):
        import ecomerce.signals  # Ensure signals are imported
        
        
        
  
