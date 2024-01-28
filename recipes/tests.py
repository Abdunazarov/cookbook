from django.urls import reverse
from .models import Product, Recipe, RecipeProduct
from django.test import TestCase

class AddProductToRecipeTests(TestCase):
    def setUp(self):
        self.product_tv = Product.objects.create(name="Творог", times_used=0)
        self.product_eg = Product.objects.create(name="Яйцо", times_used=0)
        self.product_su = Product.objects.create(name="Сахар", times_used=0)
        self.recipe = Recipe.objects.create(name="Сырники")

    def test_add_product_to_recipe(self):
        url = reverse('add_product_to_recipe')
        data_tv = {'recipe_id': self.recipe.id, 'product_id': self.product_tv.id, 'weight': 200}
        data_eg = {'recipe_id': self.recipe.id, 'product_id': self.product_eg.id, 'weight': 50}
        data_su = {'recipe_id': self.recipe.id, 'product_id': self.product_su.id, 'weight': 10}

        response_tv = self.client.get(url, data_tv)
        response_eg = self.client.get(url, data_eg)
        response_su = self.client.get(url, data_su)

        self.assertEqual(response_tv.status_code, 200)
        self.assertEqual(response_eg.status_code, 200)
        self.assertEqual(response_su.status_code, 200)

        self.assertTrue(RecipeProduct.objects.filter(recipe=self.recipe, product=self.product_tv).exists())
        self.assertTrue(RecipeProduct.objects.filter(recipe=self.recipe, product=self.product_eg).exists())
        self.assertTrue(RecipeProduct.objects.filter(recipe=self.recipe, product=self.product_su).exists())


class CookRecipeTests(TestCase):
    def setUp(self):
        self.product_tv = Product.objects.create(name="Творог", times_used=0)
        self.product_eg = Product.objects.create(name="Яйцо", times_used=0)
        self.product_su = Product.objects.create(name="Сахар", times_used=0)
        self.recipe = Recipe.objects.create(name="Сырники")
        RecipeProduct.objects.create(recipe=self.recipe, product=self.product_tv, weight=200)
        RecipeProduct.objects.create(recipe=self.recipe, product=self.product_eg, weight=50)
        RecipeProduct.objects.create(recipe=self.recipe, product=self.product_su, weight=10)

    def test_cook_recipe(self):
        url = reverse('cook_recipe')
        data = {'recipe_id': self.recipe.id}
        response = self.client.get(url, data)

        self.assertEqual(response.status_code, 200)
        self.product_tv.refresh_from_db()
        self.product_eg.refresh_from_db()
        self.product_su.refresh_from_db()
        self.assertEqual(self.product_tv.times_used, 1)
        self.assertEqual(self.product_eg.times_used, 1)
        self.assertEqual(self.product_su.times_used, 1)


class ShowRecipesWithoutProductTests(TestCase):
    def setUp(self):
        self.product_tv = Product.objects.create(name="Творог", times_used=0)
        self.recipe_with_product = Recipe.objects.create(name="Сырники")
        self.recipe_without_product = Recipe.objects.create(name="Блины")
        RecipeProduct.objects.create(recipe=self.recipe_with_product, product=self.product_tv, weight=200)


    def test_show_recipes_without_product(self):
        url = reverse('show_recipes_without_product')
        data = {'product_id': self.product_tv.id}
        response = self.client.get(url, data)

        self.assertEqual(response.status_code, 200)
