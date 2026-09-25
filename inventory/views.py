from django.shortcuts import get_object_or_404, render

from .models import Product


def product_list(request):
    products = Product.objects.filter(active=True).order_by("name")

    return render(
        request,
        "inventory/product_list.html",
        {"products": products},
    )


def label_preview(request, pk):
    product = get_object_or_404(
        Product.objects.prefetch_related("recipe_ingredients__ingredient"),
        pk=pk,
        active=True,
    )

    recipe_ingredients = (
        product.recipe_ingredients
        .select_related("ingredient")
        .order_by("label_order", "id")
    )

    return render(
        request,
        "inventory/label_preview.html",
        {
            "product": product,
            "recipe_ingredients": recipe_ingredients,
        },
    )