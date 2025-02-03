import pickle
import streamlit as st
import requests


def get_movie_poster(movie_id):
    api_key = "8265bd1679663a7ea12ac168da84d2e8"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return None


def get_similar_movies(movie_title):
    movie_index = movies[movies['title'] == movie_title].index[0]
    distances = sorted(enumerate(similarity[movie_index]), reverse=True, key=lambda x: x[1])
    movie_names = []
    movie_posters = []
    for movie_index, similarity_score in distances[1:6]:
        similar_movie_id = movies.iloc[movie_index].movie_id
        poster_url = get_movie_poster(similar_movie_id)
        if poster_url:
            movie_posters.append(poster_url)
            movie_names.append(movies.iloc[movie_index].title)
    return movie_names, movie_posters


st.header('Movie Recommender System')

movies = pickle.load(open('movies_list.pkl', 'rb'))
similarity = pickle.load(open('similarities.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or Select a Movie from Dropdown", movie_list, placeholder='Select Movie')

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = get_similar_movies(selected_movie)
    num_recommendations = min(10, len(recommended_movie_names))
    cols = st.columns(num_recommendations)

    for i in range(num_recommendations):
        with cols[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i], use_column_width=True)
