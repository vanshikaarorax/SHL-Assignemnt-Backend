from flask import Blueprint, request, jsonify
from flask_cors import cross_origin  # Import the cross_origin decorator
from dataset import get_dataset
from recommendation import recommend_agents

# Blueprint for main routes
main_routes = Blueprint('main', __name__)

# Home route (optional)
@main_routes.route('/', methods=['GET'])
def home():
    return "Welcome to the Flask app!"

# Route for recommendations
@main_routes.route('/recommend', methods=['GET'])
@cross_origin(origins=["https://your-app-frontend.onrender.com"])  # Update with your production frontend URL
def recommend():
    try:
        # Get user query from the query parameters
        user_query = request.args.get("query", "").strip()
        if not user_query:
            return jsonify({"error": "No query provided"}), 400

        # Load dataset
        dataset = get_dataset()

        # Get recommendations based on user query
        recommendations = recommend_agents(user_query, dataset)

        # Convert recommendations to list of dictionaries
        recommendations_list = recommendations.to_dict(orient='records')

        # Return recommendations as JSON
        return jsonify(recommendations_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route for search
@main_routes.route('/search', methods=['GET'])
@cross_origin(origins=["https://your-app-frontend.onrender.com"])  # Update with your production frontend URL
def search_tests():
    try:
        # Get search query from the request
        query = request.args.get("query", "").strip()
        if not query:
            return jsonify({"error": "No query provided"}), 400

        # Load dataset
        dataset = get_dataset()

        # Perform a search based on the query
        search_results = dataset[dataset['name'].str.contains(query, case=False, na=False)]

        # Convert results to list of dictionaries
        search_results_list = search_results.to_dict(orient='records')

        # Return the search results as JSON
        return jsonify(search_results_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
