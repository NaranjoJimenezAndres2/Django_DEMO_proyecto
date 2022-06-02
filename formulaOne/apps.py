from django.apps import AppConfig


class FormulaOneConfig(AppConfig):  #esto se tiene que poner en el settings.py de la aplicacion
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'formulaOne'
