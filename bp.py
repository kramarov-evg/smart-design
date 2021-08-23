import json

from bson import ObjectId, json_util
from extensions import mongo
from flask import jsonify, Blueprint, abort, request
from utils import construct_criteria, error_to_json
from werkzeug.exceptions import BadRequest, UnprocessableEntity, NotFound

bp = Blueprint('test', __name__)

# Endpoint for adding items. Accepts item's fields as json
@bp.route('/products/add', methods=['POST'])
def add_product():
    new_product = {}
    try:
        new_product['name'] = request.json['name']
        new_product['description'] = request.json['description']
    except KeyError as e:
        abort(UnprocessableEntity)
    extra_params = request.json.get('params', None)
    if extra_params is not None:
        try:
            new_product['params'] = dict(extra_params)
        except:
            abort(BadRequest)
    inserted_val = mongo.db.products.insert_one(new_product)
    return product_details_by_id(inserted_val.inserted_id)

# Endpoint to search items. Accepts search criterias as json
@bp.route('/products/search', methods=['POST'])
def search_product():
    query_criterias = {}
    requested_name = request.json.get('name', None)
    if requested_name:
        try:
            name_criteria = construct_criteria(requested_name)
        except ValueError:
            abort(UnprocessableEntity)
        query_criterias['name'] = name_criteria
        request.json.pop('name')
    for param_name in request.json.keys():
        try:
            criteria = construct_criteria(request.json[param_name])
        except ValueError:
            abort(UnprocessableEntity)
        real_param_name = f'params.{param_name}'
        query_criterias[real_param_name] = criteria

    products = mongo.db.products.find(query_criterias)
    products_sanitazied = json.loads(json_util.dumps(products))
    return jsonify(products_sanitazied)

# Endpoint to get info on single item
@bp.route('/products/<ObjectId:id>', methods=['GET'])
def product_details_by_id(id):
    product = mongo.db.products.find_one_or_404({'_id': ObjectId(id)})
    product_sanitazied = json.loads(json_util.dumps(product))
    return jsonify(product_sanitazied)


@bp.errorhandler(BadRequest)
def bad_request_to_json(error):
    return error_to_json(error)


@bp.errorhandler(NotFound)
def not_found_to_json(error):
    return error_to_json(error)


@bp.errorhandler(UnprocessableEntity)
def uprocessable_to_json(error):
    return error_to_json(error)