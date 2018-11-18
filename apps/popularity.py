# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from sqlalchemy import create_engine
from datetime import date as dt



from app import app

engine = create_engine('postgres://biancabartolomei:19972015@localhost:5432/spotify')
df_top10_track = pd.read_sql_query("select * from spotify_db.top10_tracks('2018-10-23 00:00:00.000000')",con=engine)
df_top10_artist = pd.read_sql_query("select * from spotify_db.top10_artist('2018-10-23 00:00:00.000000')",con=engine)
df_popularity = pd.read_sql_query("select * from spotify_db.top_musicas_populares", con=engine)
track_id_dec = engine.execute("select * from spotify_db.maior_decrescimo()").cursor.fetchall()[0][0]
track_id_cres = engine.execute("select * from spotify_db.maior_crescimento()").cursor.fetchall()[0][0]

# ======================================================================================================================
def update_dropdown_track():
    musicas = []
    opt_track = []
    for track, track_id, artist_name in \
            zip(df_popularity['track_name'], df_popularity['track_id'], df_popularity['artist_name']):

        if track_id not in musicas and track is not None:
            a = {'label':track+' - '+artist_name, 'value':track_id}
            opt_track.append(a)
            musicas.append(track_id)
    return opt_track

# ======================================================================================================================
page_top_10 =  html.Div([

    # Card Ranking
    html.Div([
        html.Div([
            html.Div([

                html.H6(['Ranking'],className='mdl-cell mdl-cell--12-col'),
                html.Hr([],className='mdl-cell mdl-cell--12-col'),

                # Ranking Track
                html.Div([
                    html.Div([

                    ], className='card'),
                ], className='mdl-cell mdl-cell--5-col'),

                # Data Picker
                html.Div([
                    dcc.DatePickerSingle(
                        id='date-ranking',
                        date=dt(2018, 11, 1)
                    )
                ], className='mdl-cell mdl-cell--2-col'),

                # Ranking Artist
                html.Div([
                    html.Div([

                    ], className='card'),
                ], className='mdl-cell mdl-cell--5-col'),

            ], className='mdl-grid'),
        ], className='card')
    ],className='mdl-cell mdl-cell--12-col', id ='card-ranking'),

    html.Div([
        html.Hr([])
    ], className='mdl-cell mdl-cell--12-col'),

    #===================================================================================================================
    # Card Comparação
    html.Div([

        html.Div([

            html.Div([

                html.H6(['Comparação'], className='titulo-grafico'),
                html.Hr([], className='mdl-cell mdl-cell--12-col'),

                # Grafico comparação
                html.Div([
                    dcc.Graph(
                        id='popularidade_musica',
                        figure={
                            'data': [
                                {'x': df_popularity['data_popularidade'],
                                 'y': df_popularity['track_popularity'],
                                 'type': 'lines',
                                 'name': df_popularity['track_name']},
                            ],
                            'layout': {
                                'xaxis': {'title': 'Data'},
                                'yaxis': {'title': 'Popularidade'}
                            }
                        }
                    ),
                ], className='mdl-cell mdl-cell--8-col'),

                # Card Dropdowns
                html.Div([
                    html.H6(['Track 1']),

                    dcc.Dropdown(
                        id='dropdown-feature-track',
                        options=update_dropdown_track(),
                        multi=False,
                        value=""
                    ),

                    html.H6(['Track 2']),

                    dcc.Dropdown(
                        id='dropdown-feature-track2',
                        options=update_dropdown_track(),
                        multi=False,
                        value=""
                    ),

                ], className='mdl-cell mdl-cell--4-col'),

            ], className='mdl-grid')

        ], className='card')

    ], className='mdl-cell mdl-cell--12-col'),

    html.Div([
        html.Hr([])
    ], className='mdl-cell mdl-cell--12-col'),

    # ===================================================================================================================
    # Card evolucao
    html.Div([

        html.Div([

            html.Div([

                html.H6(['Downgrade e Upgrade'], className='titulo-grafico'),
                html.Hr([], className='mdl-cell mdl-cell--12-col'),

                html.Div([

                    html.Div([
                        dcc.Graph(
                            id='perda-popularidade',
                            figure={
                                'data': [
                                    {'x': df_popularity.loc[df_popularity['track_id'] == track_id_dec]['data_popularidade'],
                                     'y': df_popularity.loc[df_popularity['track_id'] == track_id_dec]['track_popularity'],
                                     'type': 'lines',
                                     'marker': {'color': 'rgba(255,64,129,1)'},
                                     'name': df_popularity.loc[df_popularity['track_id'] == track_id_dec][
                                         'track_name'].iloc[0]+ ' - '+ df_popularity.loc[df_popularity['track_id'] == track_id_dec][
                                         'artist_name'].iloc[0],
                                     'showlegend': True,
                                     },

                                ],
                                'layout': {
                                    'xaxis': {'title': 'Data'},
                                    'yaxis': {'title': 'Popularidade'},
                                    'title': 'Maior perda de popularidade',
                                }
                            }
                        ),
                    ], className='card')

                ], className='mdl-cell mdl-cell--6-col'),

                html.Div([

                    html.Div([
                        dcc.Graph(
                            id='ganho-popularidade',
                            figure={
                                'data': [
                                    {'x': df_popularity.loc[df_popularity['track_id'] == track_id_cres]['data_popularidade'],
                                     'y': df_popularity.loc[df_popularity['track_id'] == track_id_cres]['track_popularity'],
                                     'type': 'lines',
                                     'name':df_popularity.loc[df_popularity['track_id'] == track_id_cres]['track_name'].iloc[0]+
                                            ' - '+ df_popularity.loc[df_popularity['track_id'] == track_id_cres][
                                         'artist_name'].iloc[0],
                                     'showlegend': True,
                                     },
                                ],
                                'layout': {
                                    'xaxis': {'title': 'Data'},
                                    'yaxis': {'title': 'Popularidade'},
                                    'title': 'Maior aumento de popularidade',

                                }
                            }
                        ),
                    ], className='card')

                ], className='mdl-cell mdl-cell--6-col'),

            ], className='mdl-grid')

        ], className='card')

    ], className='mdl-cell mdl-cell--12-col'),

    html.Div([

        html.Hr([])

    ], className='mdl-cell mdl-cell--12-col'),


            ], className='mdl-grid')


# ======================================================================================================================
@app.callback(dash.dependencies.Output('card-ranking', 'children'),
              [dash.dependencies.Input('date-ranking', 'date')])
def display_page(data):

    query = data + ' 00:00:00.000000'
    df_top10_track = pd.read_sql_query('select * from spotify_db.top10_tracks(' + "'" + query + "'"+')',
                                       con=engine)
    df_top10_artist = pd.read_sql_query('select * from spotify_db.top10_artist(' + "'" + query + "'"+')',
                                       con=engine)

    return  html.Div([
            html.Div([

                html.H6(['Ranking'], className='titulo-grafico'),
                html.Hr([], className='mdl-cell mdl-cell--12-col'),

                # Ranking Track

                html.Div([],className='mdl-cell mdl-cell--2-col'),

                html.Div([

                    html.Table(
                        # Header
                        [html.Tr(
                            [html.Th(col, className='mdl-data-table__cell--non-numeric') for col in
                             df_top10_track.columns])] +

                        # Body
                        [html.Tr([
                            html.Td(df_top10_track.iloc[i][col], className='mdl-data-table__cell--non-numeric') for
                            col
                            in
                            df_top10_track.columns
                        ]) for i in range(min(len(df_top10_track), 10))],
                        className='mdl-data-table mdl-js-data-table'
                    ),

                ], className='mdl-cell mdl-cell--3-col'),

                # Data Picker
                html.Div([
                    dcc.DatePickerSingle(
                        id='date-top10',
                        date=dt(2018, 11, 1)
                    )
                ], className='mdl-cell mdl-cell--2-col'),

                # Ranking Artist
                html.Div([

                    html.Table(
                        # Header
                        [html.Tr(
                            [html.Th(col, className='mdl-data-table__cell--non-numeric') for col in
                             df_top10_track.columns])] +

                        # Body
                        [html.Tr([
                            html.Td(df_top10_track.iloc[i][col], className='mdl-data-table__cell--non-numeric') for
                            col
                            in
                            df_top10_track.columns
                        ]) for i in range(min(len(df_top10_track), 10))],
                        className='mdl-data-table mdl-js-data-table'
                    ),

                ], className='mdl-cell mdl-cell--3-col'),

                html.Div([], className='mdl-cell mdl-cell--2-col'),

            ], className='mdl-grid'),
        ], className='card')

# ======================================================================================================================

@app.callback(
    dash.dependencies.Output('popularidade_musica','figure'),
    [dash.dependencies.Input('dropdown-feature-track', 'value'),
     dash.dependencies.Input('dropdown-feature-track2', 'value')])
def update_figure(track_input, track_input2):
    filtro = pd.DataFrame(columns=['track_id', 'track_name', 'artist_name', 'track_popularity',
                                   'data_popularidade', 'artist_genre'])
    temp = df_popularity
    filtro2 = pd.DataFrame(columns=['track_id', 'track_name', 'artist_name', 'track_popularity',
                                    'data_popularidade', 'artist_genre'])
    temp2 = df_popularity


    if track_input or track_input2:
        if track_input:
            temp = temp.loc[df_popularity['track_id'] == track_input]
            filtro = temp

        if track_input2:
            temp2 = temp2.loc[df_popularity['track_id'] == track_input2]
            filtro2 = temp2

    else:
        filtro = pd.DataFrame(columns=['track_id', 'track_name', 'artist_name', 'track_popularity',
                                       'data_popularidade', 'artist_genre'])



    traces = []

    if len(filtro['track_name']) == 0:
        legenda1 = ''
    else:
        legenda1 = filtro['track_name'].iloc[0]

    if len(filtro2['track_name']) == 0:
        legenda2 = ''
    else:
        legenda2 = filtro2['track_name'].iloc[0]

    traces.append(go.Line(
        x=filtro['data_popularidade'],
        y=filtro['track_popularity'],
        name=legenda1,
        marker=dict(
            color='rgba(39,144,176,1)',
        ),
    ))

    traces.append(go.Line(
        x=filtro2['data_popularidade'],
        y=filtro2['track_popularity'],
        name=legenda2,
        marker=dict(
            color='rgba(255,64,129,1)',
        ),
    ))
    return {
        'data': traces,
        'layout': {
                'xaxis': {'title': 'Data'},
                'yaxis': {'title': 'Popularidade'}

        }
    }


























#
# html.Div([
#         dcc.DatePickerSingle(
#             id='date-top10',
#             date=dt(2018, 11, 1)
#         )
#     ], className='mdl-cell mdl-cell--12-col'),
#
#
#
#     html.Div([
#         html.Div([
#             html.Div([
#                 html.Div([
#                     html.H3(['Track'])
#                 ], className='card')
#             ],className='mdl-cell mdl-cell--6-col'),
#             html.Div(['Artist'],className='mdl-cell mdl-cell--6-col'),
#
#             html.Div([
#                 html.Table(
#                     # Header
#                     [html.Tr(
#                         [html.Th(col, className='mdl-data-table__cell--non-numeric') for col in
#                          df_top10_track.columns])] +
#
#                     # Body
#                     [html.Tr([
#                         html.Td(df_top10_track.iloc[i][col], className='mdl-data-table__cell--non-numeric') for col
#                         in
#                         df_top10_track.columns
#                     ]) for i in range(min(len(df_top10_track), 10))], className='mdl-data-table mdl-js-data-table'
#                 ),
#             ], className='mdl-cell mdl-cell--6-col'),
#
#             html.Div([
#                 html.Table(
#                     # Header
#                     [html.Tr(
#                         [html.Th(col, className='mdl-data-table__cell--non-numeric') for col in
#                          df_top10_artist.columns])] +
#
#                     # Body
#                     [html.Tr([
#                         html.Td(df_top10_artist.iloc[i][col], className='mdl-data-table__cell--non-numeric') for col
#                         in
#                         df_top10_artist.columns
#                     ]) for i in range(min(len(df_top10_artist), 10))], className='mdl-data-table mdl-js-data-table'
#                 ),
#             ], className='mdl-cell mdl-cell--6-col'),
#
#         ],className='mdl-grid')
#     ], className='mdl-cell mdl-cell--12-col', id='top10_page')