from django.apps import AppConfig

class EduConfig(AppConfig):
    name = 'edu'

    def ready(self):
        # Import signals or perform model-related operations here
        from edu.models import create_sample_entries
        create_sample_entries()
