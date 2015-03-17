from django.conf import settings

def resource_urls(request):
    defaults = dict(
        #STATIC_URL=settings.STATIC_URL,
        SITE_NAME=settings.SITE_NAME,
        IMPACT_CLASS_URL=settings.IMPACT_CLASS_URL,
    )
    
    return defaults