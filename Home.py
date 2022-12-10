import streamlit as st
import pandas as pd
import pickle
import requests


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=5cb6ebca2cf86e07ae755fafdd0cc4a9&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:16]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Movie Recommendations")

select_movie_name = st.selectbox('Search', movies['title'].values)

if st.button('Recommend'):
    ##
    st.header(select_movie_name)
    col1, col2 = st.columns([3, 2])
    with col1:
        st.image(fetch_poster(movies[movies['title'] == select_movie_name].movie_id.values[0]))
    with col2:
        st.subheader('GENRES')
        for i in movies[movies['title'] == select_movie_name].genres.values[0]:
            st.write(i)
        st.subheader(' ')
        st.subheader(' ')

        st.subheader('RATING')
        st.subheader(movies[movies['title'] == select_movie_name].vote_average.values[0])
    st.text(' ')
    st.write('ABOUT')
    st.write(movies[movies['title'] == select_movie_name].overview.values[0])
    st.subheader(" ")
    ##
    names, posters = recommend(select_movie_name)
    st.subheader("Recommended movies")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.write(names[0])
        st.image(posters[0])

    with col2:
        st.write(names[1])
        st.image(posters[1])
    with col3:
        st.write(names[2])
        st.image(posters[2])
    with col4:
        st.write(names[3])
        st.image(posters[3])
    with col5:
        st.write(names[4])
        st.image(posters[4])

    st.subheader(' ')

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.write(names[5])
        st.image(posters[5])
    with col2:
        st.write(names[6])
        st.image(posters[6])
    with col3:
        st.write(names[7])
        st.image(posters[7])
    with col4:
        st.write(names[8])
        st.image(posters[8])
    with col5:
        st.write(names[9])
        st.image(posters[9])

    st.subheader(' ')

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.write(names[10])
        st.image(posters[10])

    with col2:
        st.write(names[11])
        st.image(posters[11])
    with col3:
        st.write(names[12])
        st.image(posters[12])
    with col4:
        st.write(names[13])
        st.image(posters[13])
    with col5:
        st.write(names[14])
        st.image(posters[14])

