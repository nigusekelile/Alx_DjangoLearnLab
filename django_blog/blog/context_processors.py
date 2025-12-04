from .utils import get_popular_tags
from .forms import SearchForm

def tags_and_search(request):
    """
    Context processor to add popular tags and search form to all templates
    """
    context = {
        'popular_tags': get_popular_tags(limit=10),
        'search_form': SearchForm(),
    }
    return context