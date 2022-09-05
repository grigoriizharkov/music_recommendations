import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render
from .forms import UserForm
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors


# TODO
#  1) dataset cleaning (done, check for recommendation quality)
#  3) expansion dataset via spotipy
#  4) frontend using React?


def parsing(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            url = user_form.cleaned_data['url']
            number = user_form.cleaned_data['number']

            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")

            tracks = soup.find_all("div", class_="d-track__overflowable-wrapper deco-typo-secondary block-layout")

            tracks_list, artists_list = list(), list()

            for track in tracks:
                track_name = track.find("a", class_="d-track__title deco-link deco-link_stronger")
                if track_name is None:
                    track_name = track.find("span", class_="d-track__title deco-typo-secondary")

                artist_name = track.find("a", class_="deco-link deco-link_muted")

                tracks_list.append(track_name.text.lstrip().rstrip())
                artists_list.append(artist_name.text.lstrip().rstrip())

            return prediction(request, tracks_list, artists_list, number)
        else:
            return HttpResponse("Invalid data")
    else:
        user_form = UserForm()

        return render(request, "form.html", {"form": user_form})


def prediction(request, tracks: list, artists: list, number=10):
    data = pd.read_csv("clean_data.csv")
    sample = pd.DataFrame({"artist_name": artists, "track_name": tracks})

    songs_indexes = list()
    for row in sample.itertuples():
        res = data[(data['track_name'] == row[2]) &
                   (data['artist_name'] == row[1])]
        if len(res) != 0:
            songs_indexes.extend(list(res.index))

    x = data.select_dtypes(np.number)
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)

    nbrs = NearestNeighbors(n_neighbors=number, algorithm='auto', metric='cosine', n_jobs=-1).fit(x_scaled)

    songs_vectors = list()
    for index in songs_indexes:
        songs_vectors.append(x_scaled[index])

    song_matrix = np.array(list(songs_vectors))
    sample_vector = np.mean(song_matrix, axis=0)

    distances, indices = nbrs.kneighbors([sample_vector])

    recommendations = list()
    for index in indices[0]:
        artists_name = data.iloc[index]['artist_name']
        tracks_name = data.iloc[index]['track_name']

        recommendations.append(artists_name + ' - ' + tracks_name)

    return render(request, "table.html", context={"tracks": recommendations})
