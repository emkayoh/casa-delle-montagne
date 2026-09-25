from django.contrib import admin

from .models import Ingredient, Product, RecipeIngredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "label_name",
        "stock_unit",
        "active",
    )
    list_filter = ("active", "stock_unit")
    search_fields = ("name", "label_name")
    ordering = ("name",)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

    fields = (
        "ingredient",
        "quantity",
        "unit",
        "label_order",
    )

    ordering = ("label_order",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "nominal_weight_g",
        "active",
    )
    list_filter = ("active",)
    search_fields = ("name", "description")
    ordering = ("name",)

    inlines = [RecipeIngredientInline]


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "ingredient",
        "quantity",
        "unit",
        "label_order",
    )
    list_filter = ("product", "unit")
    search_fields = (
        "product__name",
        "ingredient__name",
        "ingredient__label_name",
    )
    ordering = (
        "product__name",
        "label_order",
    )