from .models import Favorites, Video


def global_faves(request):
    all_faves = Favorites.objects.all().order_by('-id')[:3]
    return {
        'all_faves': all_faves
    }


def global_vids(request):
    all_vids = Video.objects.all().order_by('-id')[:8]
    return {
        'all_vids': all_vids
    }
