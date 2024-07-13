import streamlit as st
import pickle

import requests


def fetch_poster(movie_id):
    api_key = '7650cbf317132270032f652bab2cfa7b'
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=7650cbf317132270032f652bab2cfa7b'
    response = requests.get(url)
    data = response.json()
    image = data['poster_path']

    return 'https://image.tmdb.org/t/p/w500/' + image


def recommend(movie):
    movie_index = movies_df[movies_df.title == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    posters_for_movies = []
    for i in movies_list:
        movie_id = movies_df.iloc[i[0], 0]
        recommended_movies.append(movies_df.iloc[i[0]].title)
        posters_for_movies.append(fetch_poster(movie_id))
    return recommended_movies, posters_for_movies


st.title('Movie Recommend system')
st.markdown(
    '''Select a Movie Name '''
)
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_df = pickle.load(open('movies.pkl', 'rb'))

movies = movies_df['title'].values
selected_movies_name = st.selectbox(' ', movies)
st.write("You selected:", selected_movies_name)

if st.button('Recommend'):
    recommendation, posters = recommend(selected_movies_name)
    cols = list(st.columns(5))
    for title, poster , col in zip(recommendation, posters , cols):
        with col:
            st.image(poster, caption=title , use_column_width= True , width = 300)
