from flask import jsonify


def error_to_json(error):
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
