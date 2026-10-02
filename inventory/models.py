from django.db import models


class Unit(models.TextChoices):
    GRAM = "g", "g"
    MILLILITRE = "ml", "ml"
    TEASPOON = "tsp", "tsp"
    TABLESPOON = "tbsp", "tbsp"
    EACH = "each", "each"
    KILOGRAM = "kg", "kg"
    LITRE = "l", "l"
        

class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True)
    label_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Name used on the product label, if different.",
    )
    stock_unit = models.CharField(
        max_length=10,
        choices=Unit.choices,
        default=Unit.GRAM,
    )
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def display_label_name(self):
        return self.label_name or self.name


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    nominal_weight_g = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Nominal finished weight of one item in grams.",
    )

    active = models.BooleanField(default=True)

    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        related_name="products",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="recipe_ingredients",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        related_name="recipe_ingredients",
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=3,
    )

    unit = models.CharField(
        max_length=10,
        choices=Unit.choices,
        default=Unit.GRAM,
    )

    label_order = models.PositiveIntegerField(
        default=0,
        help_text="Order in which this ingredient appears on the label.",
    )

    class Meta:
        ordering = ["label_order", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "ingredient"],
                name="unique_ingredient_per_product",
            )
        ]

    def __str__(self):
        return (
            f"{self.product.name}: "
            f"{self.ingredient.name} "
            f"{self.quantity} {self.get_unit_display()}"
        )