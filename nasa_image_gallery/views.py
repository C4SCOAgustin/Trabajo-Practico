# capa de vista/presentación
# si se necesita algún dato (lista, valor, etc), esta capa SIEMPRE se comunica con services_nasa_image_gallery.py

from django.http import HttpResponse
from django.shortcuts import redirect, render

from nasa_image_gallery.layers.generic.mapper import fromTemplateIntoNASACard
from .layers.services import services_nasa_image_gallery
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# función que invoca al template del índice de la aplicación.
def index_page(request):
    return render(request, 'index.html')

# auxiliar: retorna 2 listados -> uno de las imágenes de la API y otro de los favoritos del usuario.
def getAllImagesAndFavouriteList(request):
    images = []
    favourite_list = []
    images= services_nasa_image_gallery.getAllImages()

    return images, favourite_list

# función principal de la galería.
def home(request):
    # llama a la función auxiliar getAllImagesAndFavouriteList() y obtiene 2 listados: uno de las imágenes de la API y otro de favoritos por usuario*.
    # (*) este último, solo si se desarrolló el opcional de favoritos; caso contrario, será un listado vacío [].
    images = []
    favourite_list = []
    images,favourite_list= getAllImagesAndFavouriteList(request)
    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list} )


# función utilizada en el buscador.
def search(request):
    images, favourite_list = getAllImagesAndFavouriteList(request)
    search_msg = request.POST.get('query', '')
    images= services_nasa_image_gallery.getAllImages(search_msg)

    # si el usuario no ingresó texto alguno, debe refrescar la página; caso contrario, debe filtrar aquellas imágenes que posean el texto de búsqueda.
    return render (request, 'home.html', {'images': images, 'favourite_list': favourite_list})


# las siguientes funciones se utilizan para implementar la sección de favoritos: traer los favoritos de un usuario, guardarlos, eliminarlos y desloguearse de la app.
@login_required
def getAllFavouritesByUser(request):
    if not request.user.is_authenticated:
        return redirect('login')
    favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request.user)
    return render(request, 'favourites.html', {'favourite_list': favourite_list})


@login_required
def saveFavourite(request):
    if request.method == 'POST':
        nasa_card=fromTemplateIntoNASACard(request)
        nasa_card.user=request.user
        saved=services_nasa_image_gallery.saveFavourite(nasa_card)
        if saved:
            return HttpResponse('favorito guardado correctamente')
        else:
            return HttpResponse('error al guardar favorito')
    else:
        return redirect('home')
        


@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        fav_id=request.POST.get('id')
        deleted=services_nasa_image_gallery.deleteFavourite(fav_id)
        if deleted:
            return HttpResponse('favorito eliminado correctamente')
        else:
            return HttpResponse('error al eliminar favorito')


@login_required
def exit(request):
    logout(request)
    return redirect('/')