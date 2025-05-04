import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_agents(user_query, dataset):
    """
    Recommends tests based on user input using TF-IDF and cosine similarity.

    Args:
        user_query (str): The user's input describing their requirements.
        dataset (pd.DataFrame): The dataset of available tests.

    Returns:
        pd.DataFrame: Top recommended tests with their details and similarity scores.
    """

    # Extract job level from user query (case-insensitive matching)
    job_levels = ["entry-level", "mid-level", "upper-level"]
    user_job_level = next((level for level in job_levels if level in user_query.lower()), None)

    if user_job_level:
        # Filter the dataset for matching job level
        dataset = dataset[dataset['job_levels'].str.contains(user_job_level, case=False, na=False)]

    # Combine description and category for feature vectorization
    dataset['features'] = dataset['category'] + ", " + dataset['description']

    # Initialize the TF-IDF vectorizer and fit the dataset features
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(dataset['features'])

    # Transform the user query into a vector
    user_vector = vectorizer.transform([user_query])

    # Compute similarity scores between user query and dataset
    similarity_scores = cosine_similarity(user_vector, tfidf_matrix)

    # Add similarity scores to the dataset
    dataset['similarity'] = similarity_scores[0]

    # Sort the dataset by similarity score in descending order and return the top 3 recommendations
    top_recommendations = dataset[['name', 'category', 'description', 'similarity', 'url']].sort_values(by='similarity', ascending=False).head(3)

    return top_recommendations
