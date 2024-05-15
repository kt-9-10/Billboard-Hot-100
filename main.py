import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


URL = "https://www.billboard.com/charts/hot-100/"

# 年月日の入力
date_str = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

# スクレイピングデータの取得
response = requests.get(f"{URL}{date_str}/")
soup = BeautifulSoup(response.text, "html.parser")

# 曲名リストの作成
songs = [title.get_text().strip() for title in soup.select(".o-chart-results-list__item > h3")]

# 歌手名リストの作成
artists = [title.get_text().strip() for title in soup.select("ul > li > ul > .lrv-u-flex-grow-1 > .a-font-primary-s")]

# # 結果を表示
# print(songs)
# print(artists)

# Spotifyとの認証
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        show_dialog=True,
        cache_path="token.txt",
    )
)

# 曲を検索し、URIを取得
song_uris = []
for i in range(100):
    query = f"track: {songs[i]} artist: {artists[i]} year: {date_str[0:4]}"
    try:
        results = sp.search(q=query, type='track', limit=1, market="US")
        tracks = results['tracks']['items']
        if tracks:
            song_uris.append(tracks[0]['uri'])
        else:
            print(f"Spotifyで見つからない曲: {songs[i]}")
    except Exception as e:
        print(f"曲の検索中にエラーが発生しました: {songs[i]}")

# # 結果を表示
# print(song_uris)

# 現在のユーザー情報を取得
user_info = sp.current_user()

# ユーザーIDを抽出
user_id = user_info['id']

# プレイリストの作成
playlist_name = f'{date_str} Billboard 100'
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
playlist_id = playlist['id']

# 曲をプレイリストに追加
sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_id, tracks=song_uris)

print(f'プレイリスト "{playlist_name}" に曲を追加しました。')