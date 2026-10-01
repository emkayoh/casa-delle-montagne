from django.urls import path

from . import views


app_name = "inventory"


urlpatterns = [
    path("", views.product_list, name="product_list"),

    path(
        "products/new/",
        views.product_create,
        name="product_create",
    ),
    path(
        "products/<int:pk>/edit/",
        views.product_edit,
        name="product_edit",
    ),
    path(
        "products/<int:pk>/label/",
        views.label_preview,
        name="label_preview",
    ),

    path(
        "ingredients/",
        views.ingredient_list,
        name="ingredient_list",
    ),
    path(
        "ingredients/new/",
        views.ingredient_create,
        name="ingredient_create",
    ),
    path(
        "ingredients/<int:pk>/edit/",
        views.ingredient_edit,
        name="ingredient_edit",
    ),
]