from flask import Blueprint, jsonify, request
from capstone_inventory.helpers import token_required
from capstone_inventory.models import Recs, rec_schema, recs_schema, db, User

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'some_value': 200, 'another_value': 800}


#CREATE REC API
@api.route('/recs', methods = ['POST'])
@token_required
def create_rec(current_user_token):
    name = request.json['name']
    category = request.json['category']
    location = request.json['location']
    url = request.json['url']
    phone = request.json['phone']
    image_url = request.json['image_url']
    user_token = current_user_token.token

    print(f'TESTER: {current_user_token.token}')

    rec = Recs(name, category, location, url, phone, image_url, user_token = user_token)

    db.session.add(rec)
    db.session.commit()

    response = rec_schema.dump(rec)
    return jsonify(response)


#GET ALL RECS
@api.route('/recs', methods = ['GET'])
@token_required
def get_recs(current_user_token):
    owner = current_user_token.token
    recs = Recs.query.filter_by(user_token = owner).all()
    response = recs_schema.dump(recs)
    return jsonify(response)


#GET ONE REC
@api.route('/recs/<id>', methods = ['GET'])
@token_required
def get_rec(current_user_token, id):
    rec = Recs.query.get(id)
    response = rec_schema.dump(rec)
    return jsonify(response)


#UPDATE REC BY ID
@api.route('/recs/<id>', methods = ['POST'])
@token_required
def update_rec(current_user_token, id):
    rec = Recs.query.get(id)
    print(rec)
    if rec:
        rec.name = request.json['name']
        rec.category = request.json['category']
        rec.locatoin = request.json['location']
        rec.url = request.json['url']
        rec.phone = request.json['phone']
        rec.image_url = request.json['image_url']
        rec.user_token = current_user_token.token
        db.session.commit()

        response = rec_schema.dump(rec)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That input does not exist'})


#DELETE REC BY ID
@api.route('/recs/<id>', methods = ['DELETE'])
@token_required
def delete_rec(current_user_token, id):
    rec = Recs.query.get(id)
    if rec:
        db.session.delete(rec)
        db.session.commit()
        response = rec_schema.dump(rec)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That input does not exist'})
        




#YELP API ROUTES
# @api.route('/yelp/search', methods = ['GET'])
# @token_required
# def search_yelp(request, response):
#     print('inside search yelp!!! ***********')
#     term = request.args.get('term')
#     location = request.args.get('location')
#     yelpQueryUrl = "https://api.yelp.com/v3/businesses/search?term=${0}&location=${1}".format(term, location)

#     req = request.get(yelpQueryUrl, auth = ('Authorization', 'Bearer 9dIFz0czS0BtejX04dmzLcb2E3FK9qF1Jg9EVnra0W6ln0NKkHeLXx8qIhmY4K-mWdg5Xl3vaOMUDD-R_UjC9E_QTSDgABSeAk5BhKIquTqEp_8sv4eLNxojSDIwYXYx'))
#     return req





