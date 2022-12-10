import streamlit as st
import pandas as pd
import pickle
import requests
import numpy as np
import streamlit_authenticator as stauth
from deta import Deta
from PIL import Image


movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

occurrence = pickle.load(open('occurrence.pkl', 'rb'))

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=5cb6ebca2cf86e07ae755fafdd0cc4a9&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend_user(liked_movies):
    num_of_movies = len(liked_movies)
    # movie_index_list = [movies[movies['title'] == movie].index[0]]
    movie_index_list = [movies[movies['title'] == movie].index[0] for movie in liked_movies]
    x = np.linspace(0, 0, 6000)
    for i in movie_index_list:
        x = x + occurrence[i]
    # cummulative vector of all movies
    List = []
    for i in range(4806):
        t = np.dot(x, occurrence[i])
        List.append(t)
    movie_list = sorted(list(enumerate(List)), reverse=True, key=lambda x: x[1])[num_of_movies:10 + num_of_movies]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters



deta = Deta("d0ufgqex_PrKnXdndhPz5cJf49zgkbuzDMwzASzDN")
user_db = deta.Base("user_db")


def fetch_all():
    res = user_db.fetch()
    return res.items


users = fetch_all()
usernames = [user["key"] for user in users]
passwords = [user["password"] for user in users]
names = [user["name"] for user in users]
email = [user["email"] for user in users]
liked = [user['liked'] for user in users]
hashed_passwords = stauth.Hasher(passwords).generate()

credential = {'usernames': {}}
for un, nm, pw, l in zip(usernames, names, hashed_passwords, liked):
    user_dict = {'name': nm, 'password':pw, 'liked':l}
    credential['usernames'].update({un:user_dict})

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, 'cookie_name', 'signature', cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")


if authentication_status == True:
    st.title("User Page")
    authenticator.logout("Logout", "sidebar")
    col1, col2 = st.columns([3,1])
    with col2:
        image = Image.open('img.png')
        st.image(image, caption='Profile picture')
    with col1:
        st.subheader('Welcome ' + name)

    user_info = user_db.get(username)

    st.text('')
    st.subheader('Liked Movies')

    select_movie_name = st.selectbox('Search', movies['title'].values)
    if st.button('Add'):
        if select_movie_name not in user_info['liked']:
            user_db.update({"liked": user_db.util.append(select_movie_name)}, username)


    liked_movies = user_info['liked']
    liked_movies_ids = [movies[movies['title'] == movie].movie_id.values[0] for movie in liked_movies]
    liked_movies_posters = [fetch_poster(id) for id in liked_movies_ids]
    names, posters = recommend_user(liked_movies)

    empty_image = Image.open('img_1.png')
    while len(liked_movies) < 8:
        liked_movies.append("")
        liked_movies_posters.append(empty_image)

    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    with col1:
        st.write(liked_movies[0])
        st.image(liked_movies_posters[0])
    with col2:
        st.write(liked_movies[1])
        st.image(liked_movies_posters[1])
    with col3:
        st.write(liked_movies[2])
        st.image(liked_movies_posters[2])
    with col4:
        st.write(liked_movies[3])
        st.image(liked_movies_posters[3])
    with col5:
        st.write(liked_movies[4])
        st.image(liked_movies_posters[4])
    with col6:
        st.write(liked_movies[5])
        st.image(liked_movies_posters[5])
    with col7:
        st.write(liked_movies[6])
        st.image(liked_movies_posters[6])
    with col8:
        st.write(liked_movies[7])
        st.image(liked_movies_posters[7])



    st.write()
    st.subheader("Personalized Recommendations")

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

elif authentication_status == False:
    st.error("Username/password is incorrect")

elif authentication_status == None:
    st.warning("Please enter your username and password")