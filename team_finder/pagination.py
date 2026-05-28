from django.core.paginator import Paginator


def paginate_queryset(request, queryset, per_page):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop('page', None)

    query_prefix = query_params.urlencode()

    if query_prefix:
        query_prefix = f'{query_prefix}&'

    return page_obj, query_prefix
