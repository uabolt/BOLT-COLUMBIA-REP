from django.conf import settings
from django.utils import translation


class AdminLocaleURLMiddleware:

    original_lang = None

    def __init__(self):
        self.original_lang = getattr(settings, 'LANGUAGE_CODE', settings.LANGUAGE_CODE)

    def process_request(self, request):
        if request.path.startswith('/admin'):
            request.LANG = getattr(settings, 'ADMIN_LANGUAGE_CODE', settings.LANGUAGE_CODE)
            translation.activate(request.LANG)
            request.LANGUAGE_CODE = request.LANG

    def process_response(self, request, response):

        translation.activate(self.original_lang)

        return response
