from django.shortcuts import render
from global_app.models import Image

def get_last(model):
    return model.objects.count()

def not_pk_error(request):
    """
    Is used when there is no extra parameter
    in  the url
    """
    template_name = 'error_pages/notPK.html'
    ctx = {'obj_id':get_last(Image)}
    response = render(request, template_name, ctx)
    response.status_code = 404
    return response

def hand404(request, exception):
    template_name = 'error_pages/hand404.html'
    response = render(request, template_name, {})
    response.status_code = 404
    return response