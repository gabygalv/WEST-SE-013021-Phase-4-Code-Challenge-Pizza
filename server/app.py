#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api

from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'
#GETS
@app.route('/restaurants')
def restaurants():
    return [rest.to_dict(rules=('pizzas',)) for rest in Restaurant.query.all()]

@app.route('/pizzas')
def pizza():
    return [za.to_dict() for za in Pizza.query.all()]

@app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
def rest_by_id(id):
    one_rest = Restaurant.query.filter_by(id=id).first()
    if one_rest == None:
        return make_response({"error": "Restaurant not found"}, 404)
    elif request.method == 'GET':
        return make_response(one_rest.to_dict(rules=('pizzas',)), 200)
#DELETE
    elif request.method == 'DELETE':
        db.session.delete(one_rest)
        db.session.commit()
        return make_response('', 204)
#POST
@app.route('/restaurant_pizzas', methods = ['POST'])
def post_rp():
    new = request.get_json()
    new_rp = RestaurantPizza(
        price = new['price'],
        pizza_id = new['pizza_id'],
        restaurant_id = new['restaurant_id']
    )
    db.session.add(new_rp)
    db.session.commit()
    try:
        return make_response(new_rp.to_dict(rules=('pizza', '-restaurant')), 201)
    except ValueError:
        return make_response({'error': ['Invalid input']}, 400) 
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
