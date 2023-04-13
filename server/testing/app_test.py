import json
from os import environ
from flask import request

from app import app
from models import db, Restaurant, RestaurantPizza, Pizza

class TestApp:
    '''Flask application in app.py'''

    def test_creates_restaurant_pizzas(self):
        '''can POST new restaurant_pizzas through "/restaurant_pizzas" route.'''

        with app.app_context():
            RestaurantPizza.query.delete()
            Pizza.query.delete()
            Restaurant.query.delete()

            pizza = Pizza(name = 'Cheese', ingredients = "Dough, Tomato Sauce, Cheese")
            restaurant = Restaurant(name = "Karen's Lobster Shack", address = 'address1')
            db.session.add(pizza)
            db.session.add(restaurant)
            db.session.commit()
            response = app.test_client().post(
                '/restaurant_pizzas',
                data={
                    "price": 3,
                    "pizza_id": pizza.id,
                    "restaurant_id": restaurant.id,
                }
            )

            rf = RestaurantPizza.query.filter_by(restaurant=restaurant).first()
            # assert response.json['price'] == 3
            assert response.status_code == 201
            assert response.content_type == 'application/json'
            assert rf.id

    def test_restaurants(self):

        with app.app_context():
            RestaurantPizza.query.delete()
            Pizza.query.delete()
            Restaurant.query.delete()
            restaurant = Restaurant(name = "Karen's Lobster Shack", address = 'address1')
            db.session.add(restaurant)
            db.session.commit()

            response = app.test_client().get('/restaurants')
            data = json.loads(response.data.decode())
            assert(type(data) == list)
            for record in data:
                assert(type(record) == dict)
                assert(record['id'])
                assert(record['name'])
                assert(record['address'])

            db.session.delete(restaurant)
            db.session.commit()

    def test_restaurants_id(self):
        '''can get restaurant using ID "restaurants/<int:id>" route.'''

        with app.app_context():

            RestaurantPizza.query.delete()
            Pizza.query.delete()
            Restaurant.query.delete()
            restaurant = Restaurant(name = "Karen's Lobster Shack", address = 'address1')
            db.session.add(restaurant)
            db.session.commit()

            response = app.test_client().get('/restaurants/1')
            data = json.loads(response.data.decode())
            assert(type(data) == dict)
            assert(data['id'])
            assert(data['name'])
            assert(data['address'])

            db.session.delete(restaurant)
            db.session.commit()


    def test_deletes_restaurant(self):
        '''can DELETE restaurant through "restaurants/<int:id>" route.'''
        with app.app_context():

            RestaurantPizza.query.delete()
            Pizza.query.delete()
            Restaurant.query.delete()
            cheese = Pizza(name = "Emma", ingredients = "Dough, Tomato Sauce, Cheese")            
            restaurant = Restaurant(name = "Karen's Pizza Shack", address = 'address1')
            pizza_restaurant = RestaurantPizza(price = 3, restaurant = restaurant, pizza = cheese)
            db.session.add(restaurant)
            db.session.add(pizza_restaurant)

            db.session.commit()

            response = app.test_client().delete(
                f'/restaurant/{restaurant.id}'
            )
            assert(not Restaurant.query.filter_by(name="Karen's Lobster Shack").first())
    
    def test_validates_restaurantpizza_price(self):
        '''returns an error message if a POST request to /restaurantpizza contains a "price"between 1 and 30'''


        with app.app_context():
            RestaurantPizza.query.delete()
            Pizza.query.delete()
            Restaurant.query.delete()

            pizza = Pizza(name = 'Cheese', ingredients = "Dough, Tomato Sauce, Cheese")
            restaurant = Restaurant(name = "Karen's Lobster Shack", address = 'address1')
            db.session.add(pizza)
            db.session.add(restaurant)
            db.session.commit()
            response = app.test_client().post(
                '/restaurant_pizzas',
                data={
                    "price": -1,
                    "pizza_id": pizza.id,
                    "restaurant_id": restaurant.id,
                }
            ).json

            assert response['error'] == "Invalid input"
