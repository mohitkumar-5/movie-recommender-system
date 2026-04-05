import streamlit as st
import pickle
import requests

# 🔑 YOUR API KEY
API_KEY = "39f57565a9b5f73f8c51571f6501bb8e"

# =========================
# LOAD DATA
# =========================
movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# =========================
# FETCH POSTER
# =========================
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    
    data = requests.get(url).json()
    
    poster_path = data.get('poster_path')

    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/300x450?text=No+Image"

# =========================
# RECOMMEND FUNCTION
# =========================
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[movie_index])),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    names = []
    posters = []

    for i in distances:
        movie_id = movies.iloc[i[0]].id   # ✅ FIXED HERE
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))

    return names, posters

# =========================
# UI
# =========================
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox(
    "Select a movie",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)

    st.subheader("Recommended Movies:")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(posters[0])
        st.text(names[0])

    with col2:
        st.image(posters[1])
        st.text(names[1])

    with col3:
        st.image(posters[2])
        st.text(names[2])

    with col4:
        st.image(posters[3])
        st.text(names[3])

    with col5:
        st.image(posters[4])
        st.text(names[4])