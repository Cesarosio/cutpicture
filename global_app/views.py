from os.path import splitext, split

import numpy as np
import cv2

from django.shortcuts import redirect, render
from django.urls import path, reverse_lazy
from django.http import HttpResponse
from django.views import View
from django.views.generic import DetailView

from .path_utils import (
    DirProcess,
    path_join,
    get_extension,
    extension_isvalid
)
from .image_cutter import(
    read_resize,
    img_A1,
    img_A2,
    img_B1,
    img_B2,
    img_C1,
    img_C2,
    img_D
)
from .forms import ImageForm
from .models import Image
from error_pages.views import get_last


def static_response(file_path: str):
    """
    Returns an http response of an image
    or an static file (css and js)
    """
    with open(file_path, 'rb') as f:
        file_bytes = f.read()

    extension = get_extension(file_path)

    def inside(request):
        if extension in ('PNG', 'png', 'jpg'):
            return HttpResponse(file_bytes, content_type = f'image/{extension}')

        elif extension == 'css':
            return HttpResponse(file_bytes, content_type = 'text/css')

        elif extension == 'js':
            return HttpResponse(file_bytes, content_type = 'application/javascript')

    return inside


class RedirectDetailView(DetailView):
    """
    Returns a redirect if the pk in the url
    doesn't return an object
    """
    def get(self, request, *args, **kwargs):

        # Get the extra parameter in the url
        pk = self.kwargs.get('pk')

        # Check if the object exists
        obj = self.model.objects.filter(pk = pk)
        exists = obj.exists()

        if not exists:
            # Get the file path without extension
            filename = splitext(self.template_name)[0]

            # Get the file path wihout 'global_app'
            filename = ''.join(split(filename)[1:])

            # Get the url name of the file
            filename = filename.replace('/', '_')

            # Specify it has no parameters
            rev_url = f"global_app:{filename}_"

            # Redirect to the url
            return redirect(reverse_lazy(rev_url))

        return super().get(request, *args, **kwargs)


def to_detail(url : str, template_name : str, model,
            name : str, **kwargs) -> list([path]):
    """
    Makes a path of DetailView to use in dir_to_url
    """
    urlpatterns = [
        path(
            f"{url}<int:pk>",
            RedirectDetailView.as_view(
                model = Image,
                template_name = template_name,
                ),
            name = name
        )
    ]
    return urlpatterns


def to_template(**kwargs):
    """
    You can pass it as kwargs the route, the
    displayed function, and the name
    url = ...
    func = ...
    name = ...
    """
    return [
        path(
            kwargs['url'],
            kwargs['func'],
            name = kwargs['name'] + '_')
            ]


def dir_to_url(path_to_dir : str, mode='detail'):
    """
    Converts a directory into django url
    (using DetailView with extra)

    You can change mode to a function you want
    to return in order to return error pages.
    """
    file_lst = DirProcess(path_to_dir).all_files()
    lst = []

    if mode == 'detail':
        func = to_detail
    else:
        func = to_template

    for file in file_lst:

        file_path = path_join(path_to_dir, file)

        if extension_isvalid(file, ('jpg', 'png', 'PNG', 'css', 'js')):
            lst += [
                path(file, static_response(file_path))
                ]
            continue

        # else:
        filename = splitext(file)[0]
        name = filename.replace('/', '_')

        lst += func(
            url = f"{filename}/",
            template_name = f"global_app/{file}",
            model = Image,
            name = name,
            func = mode
            )

    return lst


def png_bytes(image):
    """
    Makes a png image from a np.darray using opencv
    """
    return cv2.imencode('.png', image)[1].tobytes()


class ImageCreateView(View):
    """
    View to upload an image
    """
    model = Image
    form_class = ImageForm
    template_name = 'extra_templates/subirArchivo.html'

    def success_url(self):
        """
        Redirects to selecciondeorgano with the
        extra parameter of pk
        """
        return reverse_lazy(
            'global_app:verorgano',
            kwargs={'pk':self.obj.pk}
            )

    def get(self, request):
        """
        Displays the form
        """
        ctx = {'form': self.form_class()}
        return render(request, self.template_name, ctx)

    def post(self, request):
        """
        Saves byte images to the image model
        """
        img = request.FILES.get('main', False)

        if not img:
            return redirect(request.path)

        # else:

        nparray = np.frombuffer(img.read(), np.uint8)
        cv2_img = cv2.imdecode(nparray, cv2.IMREAD_COLOR)
        
        main = read_resize(cv2_img)
        obj = self.model()

        obj.main = png_bytes(main)
        obj.A1 = png_bytes(img_A1(main))
        obj.A2 = png_bytes(img_A2(main))
        obj.B1 = png_bytes(img_B1(main))
        obj.B2 = png_bytes(img_B2(main))
        obj.C1 = png_bytes(img_C1(main))
        obj.C2 = png_bytes(img_C2(main))
        obj.D = png_bytes(img_D(main))

        obj.save()
        self.obj = obj

        return redirect(self.success_url())


class PngBaseResponse(View):
    """
    Returns png bytes with content_type = "image/png"
    """
    model = Image
    attr = None

    def get(self, request, pk):
        obj = self.model.objects.get(pk = pk)
        bytes_ = getattr(obj, self.attr)
        return HttpResponse(bytes_, content_type='image/png')


# Not using CamelCase in order to make it easier to split __name__
class Main(PngBaseResponse): attr = 'main'
class A1_Liver(PngBaseResponse): attr = 'A1'
class A2_Spleen(PngBaseResponse): attr = 'A2'
class B1_Rkidney(PngBaseResponse): attr = 'B1'
class B2_Lkidney(PngBaseResponse): attr = 'B2'
class C1_Rureter(PngBaseResponse): attr = 'C1'
class C2_Lureter(PngBaseResponse): attr = 'C2'
class D_Bladder(PngBaseResponse): attr = 'D'


class_tuple = (
    Main,
    A1_Liver,
    A2_Spleen,
    B1_Rkidney,
    B2_Lkidney,
    C1_Rureter,
    C2_Lureter,
    D_Bladder
)


def responses_from_pk(class_tup : tuple) -> list([path]):
    """
    Gets a list of classes that receive request and pk
    and returns their correspondent urlpatterns
    """
    urlpatterns = []
    for c in class_tup:
        url_name = f"{c.__name__.split('_')[0]}"
        urlpatterns += [
            path(
                f"{url_name}/<int:pk>", c.as_view(), name = url_name
                )
            ]

    return urlpatterns


def responses_nopk(class_tup : tuple, error_func) -> list([path]):
    """
    Gets a list of classes that should receive pk, but
    don't receive it, in order to display an error
    """
    urlpatterns = []
    for c in class_tup:
        url_name = f"{c.__name__.split('_')[0]}".lower()
        urlpatterns += [
            path(
                f"{url_name}/", error_func, name = f"{url_name}_"
                )
            ]

    return urlpatterns

redir_notpk = lambda request : redirect(reverse_lazy('global_app:notpk'))

organ_patterns = responses_from_pk(class_tuple)
organ_error_patterns = responses_nopk(
    class_tuple,
    redir_notpk
    )


def home(request):
    template_name = 'extra_templates/home.html'
    ctx = {'last':get_last(Image)}
    return render(request, template_name, ctx)


class HomeDetail(DetailView):
    model = Image
    template_name = 'extra_templates/home_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['last'] = get_last(self.model)
        return ctx
