from django import forms
from django.forms import inlineformset_factory

from .models import Ingredient, Product, RecipeIngredient


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = [
            "name",
            "label_name",
            "stock_unit",
            "description",
            "active",
        ]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "nominal_weight_g",
            "active",
        ]


RecipeIngredientFormSet = inlineformset_factory(
    Product,
    RecipeIngredient,
    fields=[
        "ingredient",
        "quantity",
        "unit",
        "label_order",
    ],
    extra=1,
    can_delete=True,
)