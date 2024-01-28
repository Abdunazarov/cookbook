from django.urls import reverse
from .models import Product, Recipe, RecipeProduct
from django.test import TestCase

class AddProductToRecipeTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Творог", times_used=0)
        self.recipe = Recipe.objects.create(name="Сырники")

    def test_add_product_to_recipe(self):
        url = reverse('add_product_to_recipe')
        data = {
            'recipe_id': self.recipe.id,
            'product_id': self.product.id,
            'weight': 200
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(RecipeProduct.objects.filter(recipe=self.recipe, product=self.product).exists())


class CookRecipeTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Творог", times_used=0)
        self.recipe = Recipe.objects.create(name="Сырники")
        RecipeProduct.objects.create(recipe=self.recipe, product=self.product, weight=200)

    def test_cook_recipe(self):
        url = reverse('cook_recipe')
        data = {'recipe_id': self.recipe.id}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.times_used, 1)


class ShowRecipesWithoutProductTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Творог", times_used=0)
        self.recipe_with_product = Recipe.objects.create(name="Сырники")
        self.recipe_without_product = Recipe.objects.create(name="Блины")
        RecipeProduct.objects.create(recipe=self.recipe_with_product, product=self.product, weight=200)

    def test_show_recipes_without_product(self):
        url = reverse('show_recipes_without_product')
        data = {'product_id': self.product.id}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.recipe_with_product.name)
        self.assertContains(response, self.recipe_without_product.name)
