import streamlit as st
import pandas as pd
import pickle
import requests

# Load movie data
movies_df = pd.read_pickle(r"C:\Users\Prabal Kuinkel\Desktop\Data Analyst\Movie_Recomendor_System\Data Sets\movies.pkl")
movies_list = movies_df['title'].values
similarity = pickle.load(open(r"C:\Users\Prabal Kuinkel\Desktop\Data Analyst\Movie_Recomendor_System\Data Sets\similarity.pkl", 'rb'))

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Function to recommend movies
def recommend(movie):
    for index, m in enumerate(movies_list):
        if m == movie:
            distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6]
            recommended_movies = []
            recommended_movie_posters = []
            for i in distances:
                movie_id = movies_df.iloc[i[0]]['id']  # Assuming 'movie_id' is a column in your DataFrame
                recommended_movie_posters.append(fetch_poster(movie_id))
                recommended_movies.append(movies_list[i[0]])
            return recommended_movies, recommended_movie_posters

# Streamlit UI
st.title("Movie Recommender System")

selected_movie_name = st.selectbox('Please Select a Movie:', movies_list)

if st.button('Show Recommendations'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    if recommended_movie_names and recommended_movie_posters:
        for name, poster in zip(recommended_movie_names, recommended_movie_posters):
            st.text(name)
            st.image(poster, use_column_width=True)
    else:
        st.write("No recommendations found.")
