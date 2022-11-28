from locust import HttpUser, task, between
from random import randint


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task(2)
    def view_foods(self):
        print('View foods')
        category_id = randint(2, 6)
        self.client.get(
            f'/restaurant/foods/?category_id={category_id}', name='/restaurant/foods')

    @task(4)
    def view_food(self):
        print('View food details')
        food_id = randint(1, 1000)
        self.client.get(
            f'/restaurant/foods/{food_id}', name='/restaurant/foods/:id')

    @task(1)
    def add_to_cart(self):
        print('Add to cart')
        food_id = randint(1, 10)
        self.client.post(
            f'/restaurant/carts/{self.cart_id}/cartitem_set/',
            name='/restaurant/carts/cartitem_set',
            json={'food_id': food_id, 'quantity': 1}
        )

    def on_start(self):
        response = self.client.post('/restaurant/carts/')
        result = response.json()
        self.cart_id = result['id']
