from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import F, Sum, Q
from django.db import transaction
from .models import Product, Recipe, RecipeProduct


def add_product_to_recipe(request):
    try:
        recipe_id = int(request.GET.get("recipe_id"))
        product_id = int(request.GET.get("product_id"))
        weight = int(request.GET.get("weight"))
    except (ValueError, TypeError):
        return JsonResponse({"error": "Invalid or missing parameters"}, status=400)

    recipe = get_object_or_404(Recipe, pk=recipe_id)
    product = get_object_or_404(Product, pk=product_id)

    _, created = RecipeProduct.objects.update_or_create(
        recipe=recipe, product=product, defaults={"weight": weight}
    )

    action = "created" if created else "updated"
    return JsonResponse({"success": f"Recipe product {action}"})


@transaction.atomic
def cook_recipe(request):
    recipe_id = request.GET.get("recipe_id")
    if not recipe_id:
        return JsonResponse({"error": "Missing recipe_id"}, status=400)

    recipe = get_object_or_404(Recipe, pk=recipe_id)

    products_in_recipe = recipe.products.all()

    products_in_recipe.update(times_used=F("times_used") + 1)

    return JsonResponse({"success": "Recipe has been cooked"})


def show_recipes_without_product(request):
    product_id = request.GET.get("product_id")
    if not product_id:
        return JsonResponse({"error": "Missing product_id"}, status=400)

    get_object_or_404(Product, pk=product_id)

    recipes = (
        Recipe.objects.annotate(
            total_weight=Sum(
                "recipeproduct__weight",
                filter=Q(recipeproduct__product_id=product_id),
                distinct=True,
            )
        )
        .exclude(Q(recipeproduct__isnull=True) | Q(total_weight__gte=10))
        .values_list("id", "name")
        .distinct()
    )

    context = {"recipes": [{"id": id, "name": name} for id, name in recipes]}
    return render(request, "recipes_without_product.html", context)
