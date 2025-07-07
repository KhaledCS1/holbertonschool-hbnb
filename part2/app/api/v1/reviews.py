"""Review API endpoints"""
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')
facade = HBnBFacade()

# Define models
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        try:
            review_data = api.payload
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user.id,
                'place_id': new_review.place.id
            }, 201
        except ValueError as e:
            api.abort(400, str(e))
    
    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Get all reviews"""
        reviews = facade.get_all_reviews()
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating
        } for review in reviews], 200

@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id if review.user else None,
            'place_id': review.place.id if review.place else None
        }, 200
    
    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review"""
        try:
            review_data = api.payload
            updated_review = facade.update_review(review_id, review_data)
            if not updated_review:
                api.abort(404, "Review not found")
            return {'message': 'Review updated successfully'}, 200
        except ValueError as e:
            api.abort(400, str(e))
    
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        if facade.delete_review(review_id):
            return {'message': 'Review deleted successfully'}, 200
        api.abort(404, "Review not found")

@api.route('/places/<string:place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'Reviews for place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
        
        reviews = facade.get_reviews_by_place(place_id)
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id if review.user else None
        } for review in reviews], 200