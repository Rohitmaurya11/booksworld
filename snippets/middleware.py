from .models import VisitorCount

class VisitorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        obj, created = VisitorCount.objects.get_or_create(id=1)
        obj.count += 1
        obj.save()
        return self.get_response(request)
