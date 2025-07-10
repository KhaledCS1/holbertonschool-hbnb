"""Review API endpoints"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')
facade = HBnBFacade()

# Define models
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating (1-5)')
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data or review already exists')
    @api.response(401, 'Authentication required')
    @api.doc(security='Bearer')
    def post(self):
        """Create a new review (Authenticated users only)"""
        try:
            current_user_id = get_jwt_identity()
            current_user_claims = get_jwt()
            is_admin = current_user_claims.get('is_admin', False)
            
            review_data = api.payload
            place_id = review_data.get('place_id')
            
            # Get the place
            place = facade.get_place(place_id)
            if not place:
                api.abort(400, "Place not found")
            
            # Regular users cannot review their own places
            if not is_admin and place.owner.id == current_user_id:
                api.abort(400, "You cannot review your own place")
            
            # Regular users cannot review same place twice
            if not is_admin:
                user_reviews = facade.get_all_reviews()
                for review in user_reviews:
                    if review.user.id == current_user_id and review.place.id == place_id:
                        api.abort(400, "You have already reviewed this place")
            
            # Add user_id to review data
            review_data['user_id'] = current_user_id
            
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
            'rating': review.rating,
            'user_id': review.user.id if review.user else None,
            'place_id': review.place.id if review.place else None
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
    
    @jwt_required()
    @api.expect(review_update_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.doc(security='Bearer')
    def put(self, review_id):
        """Update a review (Owner or Admin only)"""
        try:
            current_user_id = get_jwt_identity()
            current_user_claims = get_jwt()
            is_admin = current_user_claims.get('is_admin', False)
            
            review = facade.get_review(review_id)
            if not review:
                api.abort(404, "Review not found")
            
            # Check if the current user created the review OR is admin
            if not is_admin and review.user.id != current_user_id:
                api.abort(403, "Unauthorized action")
            
            review_data = api.payload
            updated_review = facade.update_review(review_id, review_data)
            
            return {
                'message': 'Review updated successfully',
                'review': {
                    'id': updated_review.id,
                    'text': updated_review.text,
                    'rating': updated_review.rating
                }
            }, 200
        except ValueError as e:
            api.abort(400, str(e))
    
    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    @api.response(401, 'Authentication required')
    @api.doc(security='Bearer')
    def delete(self, review_id):
        """Delete a review (Owner or Admin only)"""
        current_user_id = get_jwt_identity()
        current_user_claims = get_jwt()
        is_admin = current_user_claims.get('is_admin', False)
        
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        
        # Check if the current user created the review OR is admin
        if not is_admin and review.user.id != current_user_id:
            api.abort(403, "Unauthorized action")
        
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