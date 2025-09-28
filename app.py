import requests
import streamlit as st
import pandas as pd
import pickle

# Function to fetch poster from TMDb API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=7e65fda6584433cb4270a0ca82b4e9ea&language=en-US"
    response = requests.get(url)
    data = response.json()

    # Check if 'poster_path' exists and is not None
    if 'poster_path' in data and data['poster_path']:
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# Function to recommend similar movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

# Load data
movie_dict = pickle.load(open("movie.pkl", 'rb'))
similarity = pickle.load(open("somilarity.pkl", 'rb'))  # fixed typo
movies = pd.DataFrame(movie_dict)

# Streamlit app
st.title('🎬 Movie Recommendation System')

selected_movie_name = st.selectbox('Choose a movie:', movies['title'])

if st.button('Recommend'):
    recommendations, posters = recommend(selected_movie_name)

    cols = st.columns(5)  # updated from st.beta_columns to st.columns

    for idx, col in enumerate(cols):
        with col:
            st.text(recommendations[idx])
            st.image(posters[idx])
