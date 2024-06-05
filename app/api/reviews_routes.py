from flask import Blueprint, jsonify, request, abort, make_response
from flask_login import login_required, current_user
from app.models import db, Review, User, List, Place
from sqlalchemy.orm import joinedload

reviews_routes = Blueprint('reviews', __name__)

# Get all reviews of Current User
@reviews_routes.route("/current")
@login_required
def current_user_reviews():
     reviews = Review.query.options(joinedload(Review.place)).filter_by(user_id=current_user.id).all()
     reviews_dicts = []
     for review in reviews:
          review_dict = review.to_dict(include_place=True)
          reviews_dicts.append(review_dict)

     return jsonify(reviews_dicts)

# GET REVIEW BY PLACE ID
@reviews_routes.route("/places/<place_id>")
@login_required
def get_review_by_shop_id(place_id):
    review = Review.query.filter(
            Review.user_id == current_user.id,
            Review.place_id == place_id
        ).first()
    print("REVIEW in back", review)
    if(review):
     return jsonify({"review": review.to_dict()})
    else:
     return jsonify("False")

#GET REVIEW BY REVIEW ID

@reviews_routes.route("/<review_id>")
@login_required
def get_review_by_reviewid(review_id):
    review = Review.query.options(joinedload(Review.place)).get(review_id)
    if(review.user_id != current_user.id):
       return jsonify({"error": "Review must belong to current user"}), 400
    if(review):
     return jsonify(review.to_dict(include_place=True))
    else:
     return jsonify({"error": "Could not find review"}), 400



# Create Review and Place
@reviews_routes.route("/create", methods=['POST'])
@login_required
def create_review_and_place():
    print('HELLO FROM CREATE ROUTE')
    body = request.get_json()
    print("BODY IN ROUTE", body)

    try:
        selected_place = body['selectedPlace']
        place_id = selected_place['id']
        print("PLACE ID", place_id)

        place = Place.query.get(place_id)

        if not place:
            place_obj = {
                "id": selected_place['id'],
                "displayName": selected_place['displayName'],
                "lat": selected_place['location']['lat'],
                "lng": selected_place['location']['lng'],
                "formattedAddress": selected_place['formattedAddress'],
            }

            if 'editorialSummary' in selected_place:
                place_obj['editorialSummary'] = selected_place['editorialSummary']

            if 'types' in selected_place:
                place_obj['types'] = ','.join(map(str, selected_place['types']))

            if 'googleMapsURI' in selected_place:
                place_obj['googleMapsUri'] = selected_place['googleMapsURI']

            if 'websiteURI' in selected_place:
                place_obj['websiteUri'] = selected_place['websiteURI']

            if 'previewImageUrl' in selected_place:
                place_obj['previewImage'] = selected_place['previewImageUrl']

            place = Place(**place_obj)
            db.session.add(place)
            db.session.commit()

            print("Created place:", place)


        if(place):
          place = place.to_dict()
          new_review = Review(
               place_id = place["id"],
               user_id = current_user.id,
               review = body['review'],
               rating = body['rating']
              )

          db.session.add(new_review)
          db.session.commit()

        return jsonify(new_review.to_dict())  # Assuming Place model has a to_dict method to serialize to JSON
    except KeyError as e:
        print(f"Missing key: {e}")
        return jsonify({"error": f"Missing key: {e}"}), 400
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred"}), 500
