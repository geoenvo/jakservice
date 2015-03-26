from django.conf import settings

def resource_urls(request):
    defaults = dict(
        #STATIC_URL=settings.STATIC_URL,
        SITE_NAME=settings.SITE_NAME,
        JAKSAFE_IMPACT_CLASS_URL=settings.JAKSAFE_IMPACT_CLASS_URL,
        JAKSAFE_IMPACT_CLASS_FILENAME=settings.JAKSAFE_IMPACT_CLASS_FILENAME,
    )
    
    return defaults