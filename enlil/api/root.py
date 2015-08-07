from flask import Blueprint

blueprint = Blueprint('root', __name__)

@blueprint.route('/', methods=['GET'])
def root():
    return 'Hey enlil'
