from .models import Resume

def resume(request):
    return {'resume': Resume.objects.last()}