import re
import unidecode
from .app import WEB_SITE_NAME
from django.shortcuts import render
def slugify(text):
    text = unidecode.unidecode(text).lower()
    return re.sub(r'[\W_]+', '-', text)
def NotAllowed(request):
    context = {
        'title': f"{WEB_SITE_NAME}-Permission Denied",
        'message': "Your are not allowed to access."
    }
    return render(request, 'alert.html', context)


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None
