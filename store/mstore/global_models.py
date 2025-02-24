from mstore.models import ProductCategory


def global_categories(*args):
    return {'categories': ProductCategory.objects.all()}