# Song Classification
Because Spotify data is fun to play with. Currently, classification of songs in 3 playlists is around 90%.

To update the csv with chosen playlists: `python3 utils.py`

To train and evaluate the classifier: `python3 main.py train`

To apply the classifier on external playlists and your short, medium, and long term top tracks: `python main.py classify`

Example classification on non-training data:
> Your short_term listening has been
> - 20.0 % lofi
> - 56.0 % party pop
> - 24.0 % sad songs
>
> Your medium_term listening has been
> - 12.0 % lofi
> - 60.0 % party pop
> - 28.0 % sad songs
>
> Your long_term listening has been
> - 2.0 % lofi
> - 44.0 % party pop
> - 54.0 % sad songs
