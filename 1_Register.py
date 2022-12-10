import streamlit as st
import streamlit_authenticator as stauth
from deta import Deta
import re

deta = Deta("d0ufgqex_PrKnXdndhPz5cJf49zgkbuzDMwzASzDN")

user_db = deta.Base("user_db")


def insert_user(username, name, email, password, phone_number, age):
    return user_db.insert({"key": username, 'name': name, 'password': password, 'email': email, 'liked': [], 'phone number': phone_number, 'age': age})

# Connect to Deta Base with your Project Key
def fetch_all():
    res = user_db.fetch()
    return res.items


users = fetch_all()
usernames = [user["key"] for user in users]

st.header("Create new account")
with st.form("form"):
    name = st.text_input("Name: ")
    username = st.text_input("Username: ")
    email = st.text_input('Email: ')
    phone = st.text_input("Phone Number: ")
    age = st.text_input("Your Age")
    password = st.text_input("Password", type='password')
    conf_password = st.text_input("Confirm Password", type='password')
    submit = st.form_submit_button("Register")
    if submit:
        if username in usernames:
            st.error("Username is taken")
        elif not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            st.error("Enter correct email id")
        elif not re.fullmatch("[0-9]{10}", phone):
            st.error("Enter correct phone number")
        elif int(age) < 18:
            st.error("You are not allowed to make an account due to age limitations")
        elif password == conf_password:
            insert_user(username, name, email, password, phone, age)
            st.success("Registered Successfully")
        else:
            st.error("Password should match")


