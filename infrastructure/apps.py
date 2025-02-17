from django.apps import AppConfig

class InfrastructureConfig(AppConfig):
    name = 'infrastructure'

    def ready(self):
        # Import your database models to ensure they are registered.
        import infrastructure.database.user_models  # Replace with your model file when created


