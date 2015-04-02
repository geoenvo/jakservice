from django.conf import settings

def resource_urls(request):
    defaults = dict(
        #STATIC_URL=settings.STATIC_URL,
        SITE_NAME=settings.SITE_NAME,
        JAKSERVICE_IMPACT_CLASS_URL=settings.JAKSERVICE_IMPACT_CLASS_URL,
        JAKSERVICE_IMPACT_CLASS_FILENAME=settings.JAKSERVICE_IMPACT_CLASS_FILENAME,
    )
    
    return defaults