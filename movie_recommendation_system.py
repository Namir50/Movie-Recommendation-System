import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

movies = pd.read_csv('movies.csv')

# Check for and handle NaN values in the 'title' and 'genres' columns
movies['title'] = movies['title'].fillna('')
movies['genres'] = movies['genres'].fillna('')

# TF-IDF Vectorization of genres
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(movies['genres'])

# Calculate cosine similarity between movies
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

def get_movie_recommendations(movie_title):
    try:
        movie_index = movies[movies['title'] == movie_title].index[0]
    except IndexError:
        return f"Movie with title '{movie_title}' not found in the dataset."

    similarity_scores = list(enumerate(cosine_similarities[movie_index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    recommended_movies = [(movies.iloc[i]['title'], similarity) for i, similarity in similarity_scores[1:11]]
    return recommended_movies

# Example: Get movie recommendations for a movie titled 'Toy Story'
movie_title = 'Toy Story (1995)'
recommendations = get_movie_recommendations(movie_title)

if isinstance(recommendations, str):
    print(recommendations)
else:
    print(f"Top 10 movie recommendations for '{movie_title}':")
    for title, similarity in recommendations:
        print(f"{title} - Similarity: {similarity:.2f}")
