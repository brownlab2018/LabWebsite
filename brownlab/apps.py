from django.apps import AppConfig


class BrownlabConfig(AppConfig):
    name = 'brownlab'

    def ready(self):
    	import brownlab.signals
