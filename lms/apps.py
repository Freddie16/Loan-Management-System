from django.apps import AppConfig

class LmsConfig(AppConfig):
    """
    Configuration class for the 'lms' app.
    This class defines settings specific to the 'lms' app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lms'