import streamlit as st
import requests
import matplotlib.pyplot as pyplot

key = 'eb172ed2'
baseurl = 'http://www.omdbapi.com/'

def search(title, rating_range):
    params = {'apikey': key, 't': title}
    r = requests.get(baseurl, params=params)
    data = r.json()
    if 'imdbRating' in data and data['imdbRating'] != 'N/A':
        rating = float(data['imdbRating'])
        if rating < rating_range[0] or rating > rating_range[1]:
            return None
    return data

st.title("Movie Info Search")

movietitle = st.text_input("Enter the movie title:")

#NEW: SLIDER FUNCTION! User can select an IMDb rating range for whatever movie they're trying to find.
rating_range = st.slider("Select IMDb Rating Range:", 0.0, 10.0, (0.0, 10.0), 0.1)

#NEW: SELECT BOX! I let the users pick do they want to see the genre info as a bar chart or pie chart.
plot_type = st.selectbox("How do you want to view the genre data?", ["Bar Chart", "Pie Chart"])

if st.button("Search"):
    result = search(movietitle, rating_range)

    if result:
        if 'Title' in result:
            st.write(f"**Title:** {result['Title']}")
            st.write(f"**Year:** {result['Year']}")
            st.write(f"**Genre:** {result['Genre']}")
            st.write(f"**Actors:** {result['Actors']}")
            st.write(f"**IMDb Rating:** {result['imdbRating']}")

            posterlink = result.get('Poster', '')
            if posterlink != 'N/A':
                st.image(posterlink, caption=f"{result['Title']} Poster", use_column_width=True)
            else:
                st.image('noimage.png',use_column_width=True)

            if plot_type == "Bar Chart":
                fig, ax = pyplot.subplots()
                ax.bar(result['Title'], result['imdbRating'], color='blue')
                ax.set_ylabel('IMDb Rating')
                ax.set_title('IMDb Rating Bar Chart')
                st.pyplot(fig) #NEW: displays matplotlib figures in streamlit apps

            elif plot_type == "Pie Chart":
                genre_counts = result['Genre'].split(', ')
                labels = list(set(genre_counts))
                sizes = [genre_counts.count(label) for label in labels]
                fig, ax = pyplot.subplots()
                ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')
                st.pyplot(fig) #NEW: displays matplotlib figures in streamlit apps

        else:
            st.write(f"Hi, I can't find a movie matching the given title and rating range.")
