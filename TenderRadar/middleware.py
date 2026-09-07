from django.utils.deprecation import MiddlewareMixin


class NoCacheHTMLMiddleware(MiddlewareMixin):
    """Stop browsers from serving a stale TenderRadar page."""

    def process_response(self, request, response):
        content_type = response.get("Content-Type", "")
        if "text/html" in content_type or "text/plain" in content_type:
            response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
            response["Pragma"] = "no-cache"
            response["Expires"] = "0"
        return response
