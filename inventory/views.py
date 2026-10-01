from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    IngredientForm,
    ProductForm,
    RecipeIngredientFormSet,
)
from .models import Ingredient, Product


def product_list(request):
    products = Product.objects.filter(active=True).order_by("name")

    return render(
        request,
        "inventory/product_list.html",
        {"products": products},
    )


def product_create(request):
    product = Product()

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        formset = RecipeIngredientFormSet(
            request.POST,
            instance=product,
        )

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                product = form.save()
                formset.instance = product
                formset.save()

            return redirect("inventory:product_list")

    else:
        form = ProductForm(instance=product)
        formset = RecipeIngredientFormSet(instance=product)

    return render(
        request,
        "inventory/product_form.html",
        {
            "form": form,
            "formset": formset,
            "product": product,
        },
    )


def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        formset = RecipeIngredientFormSet(
            request.POST,
            instance=product,
        )

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()

            return redirect("inventory:product_list")

    else:
        form = ProductForm(instance=product)
        formset = RecipeIngredientFormSet(instance=product)

    return render(
        request,
        "inventory/product_form.html",
        {
            "form": form,
            "formset": formset,
            "product": product,
        },
    )


def label_preview(request, pk):
    product = get_object_or_404(
        Product.objects.prefetch_related(
            "recipe_ingredients__ingredient"
        ),
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


def ingredient_list(request):
    ingredients = Ingredient.objects.order_by("name")

    return render(
        request,
        "inventory/ingredient_list.html",
        {"ingredients": ingredients},
    )


def ingredient_create(request):
    if request.method == "POST":
        form = IngredientForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("inventory:ingredient_list")

    else:
        form = IngredientForm()

    return render(
        request,
        "inventory/ingredient_form.html",
        {
            "form": form,
            "title": "Add ingredient",
        },
    )


def ingredient_edit(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)

    if request.method == "POST":
        form = IngredientForm(
            request.POST,
            instance=ingredient,
        )

        if form.is_valid():
            form.save()
            return redirect("inventory:ingredient_list")

    else:
        form = IngredientForm(instance=ingredient)

    return render(
        request,
        "inventory/ingredient_form.html",
        {
            "form": form,
            "ingredient": ingredient,
            "title": "Edit ingredient",
        },
    )