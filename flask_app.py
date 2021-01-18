# -*- coding: utf-8 -*-
from flask import Flask, render_template, request

import numpy as np
import pandas as pd
import datetime
from models import search_model

import asyncio


app = Flask(__name__)

app.jinja_env.globals.update(
    zip=zip,
    enumerate=enumerate
)

async def get_request(string):
    return request.form[string]

@app.route("/", methods=['GET','POST'])
def index():
    if request.method == 'GET' :
        return render_template('index.html')
    if request.method == 'POST' :
        # data = pd.read_csv('input/data.csv')
        # song_name = asyncio.run(get_request('song_name'))
        song_name = request.form['song_name']
        data_copy, search_list = search_model.return_search_results(song_name)
        if(len(search_list) == 0):
            return render_template('index.html')
        else:
            return render_template('index.html',
                search_song_name = search_list.name.tolist()[:20],
                search_song_artists = search_list.artists.tolist()[:20],
                search_song_id = search_list.id.tolist()[:20],
                data_song_name = data_copy.name.tolist(),
                data_song_artists = data_copy.artists.tolist(),
                data_song_id = data_copy.id.tolist()
                )

@app.route("/result", methods=['GET','POST'])
def result():
    if request.method == 'GET' :
        return render_template('result.html')
    if request.method == 'POST' :
        # selected_song_id = asyncio.run(get_request('selected_song_id'))
        # data = pd.read_csv('input/data.csv')
        selected_song_id = request.form['selected_song_id']
        recommend_data = search_model.recommend_songs(selected_song_id)
        song_feat, selected_song_name = search_model.song_analysis(selected_song_id)
        return render_template('result.html', 
        selected_song_id = str(selected_song_id),
        selected_song_name = selected_song_name,
        energy = song_feat.energy.tolist()[0],
        danceability = song_feat.danceability.tolist()[0],
        tempo = song_feat.tempo.tolist()[0],
        valence = song_feat.valence.tolist()[0],
        loudness = song_feat.loudness.tolist()[0],
        acousticness = song_feat.acousticness.tolist()[0],
        recommend_song_name = recommend_data.name.tolist(),
        recommend_song_artist = recommend_data.artists.tolist()
        )

if __name__ == '__main__':
    app.run(debug = True)
