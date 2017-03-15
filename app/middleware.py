from django.http import Http404

from app.settings import DEVELOPMENT


class ProtectAdminMiddleware(object):
    def process_request(self, request):
        if not DEVELOPMENT:
            if request.path.startswith("/admin") and request.META["SERVER_PORT"] != "9678":
                raise Http404
