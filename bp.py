import json

from bson import ObjectId, json_util
from extensions import mongo
from flask import jsonify, Blueprint, abort, request
from werkzeug.exceptions import BadRequest, UnprocessableEntity

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


@bp.route('/products/<ObjectId:id>', methods=['GET'])
def product_details_by_id(id):
    product = mongo.db.products.find_one_or_404({'_id': ObjectId(id)})
    product_sanitazied = json.loads(json_util.dumps(product))
    return jsonify(product_sanitazied)


@bp.errorhandler(BadRequest)
def bad_request_to_json(error):
    error_code = error.code
    return jsonify({
        'code': error.code,
        'name': error.name,
        'message': error.description
    })


def construct_criteria(queried_field):
    string_methods_to_regexps = {
        'exact': '^{}$',
        'startsWith': '^{}',
        'endsWith': '{}$',
        'contains': '{}'
    }
    numeric_methods_to_criterias = {
        'equal': '$eq',
        'greaterThan': '$gt',
        'lessThan': '$lt',
        'greaterEqual': '$gte',
        'lessEqual': '$lte',
        'notEqual': '$ne'
    }
    criteria = None
    # Just a default value to avoid overwriting in each if for regexes
    criteria_type = '$regex'
    if queried_field:
        pattern = queried_field.get('pattern', None)
        if pattern is None:
            raise ValueError('Filtered query requires a pattern to search for')
        method = queried_field.get('method', None)
        if method in string_methods_to_regexps.keys():
            criteria = string_methods_to_regexps[method].format(pattern)
        elif method in numeric_methods_to_criterias.keys():
            criteria = pattern
            criteria_type = numeric_methods_to_criterias[method]
        else:
            raise ValueError('Invalid value for "method"')
    if criteria is not None:
        return {criteria_type: criteria}
    else:
        return None
