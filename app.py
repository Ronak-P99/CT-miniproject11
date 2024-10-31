from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
playlists = {}
songs = {}

class Song:
    def __init__(self, title, artist, genre):
        self.title = title
        self.artist = artist
        self.genre = genre
    
    def __str__(self):
        return f"{self.title} by {self.artist} and genre is {self.genre}"
    
    def __lt__(self, other):
        return self.title < other.title

class Node:
    def __init__(self, song):
        self.song = song
        self.next = None
        self.prev = None

class Playlist:
    def __init__(self, name):
        self.name = name
        self.head = None
        self.tail = None

    def add_song(self, song):
        new_node = Node(song)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def delete_song(self, title):
        current = self.head
        while current:
            if current.song.title == title:
                if current == self.head:
                    self.head = current.next
                    if self.head:
                        self.head.prev = None
                if current == self.tail:
                    self.tail = current.prev
                    if self.tail:
                        self.tail.next = None
                if current.prev:
                    current.prev.next = current.next
                if current.next:
                    current.next.prev = current.prev
                return True
            current = current.next
        return False

    def bubble_sort(self):
        if not self.head or not self.head.next:
            return

        swapped = True
        while swapped:
            swapped = False
            current = self.head
            while current.next:
                if current.song > current.next.song:
                    current.song, current.next.song = current.next.song, current.song
                    swapped = True
                current = current.next

    def search_song(self, song_title):
        current = self.head
        while current is not None:
            if current.song.title == song_title:
                return current
            current = current.next
        return None

    def display_playlist(self):
        songs = []
        current = self.head
        while current:
            # Append song details as a dictionary
            songs.append({
                "title": current.song.title,
                "artist": current.song.artist,
                "genre": current.song.genre
            })
            current = current.next
        return songs


@app.route('/songs', methods=['POST'])
def add_songs():
        data = request.get_json()
        song_title = data.get('song_title')
        song_artist = data.get('song_artist')
        song_genre = data.get('song_genre')

        if song_title in songs:
            return jsonify({"message": "Song Exists"}), 201

        songs[song_title] = Song(song_title, song_artist, song_genre)
        return jsonify({"message": "Song added successfully."}), 201

@app.route('/playlists', methods=['POST'])
def add_playlist():
        data = request.get_json()
        playlist_name = data.get('playlist_name')

        if playlist_name in playlists:
            return jsonify({"message": "Playlist Exists"}), 201
        playlists[playlist_name] = Playlist(playlist_name)
        print("Created a new playlist")

        return jsonify({"message": "Playlist added successfully."}), 201

@app.route('/playlists/<string:playlist_name>/add-song', methods=['POST'])
def add_song_to_playlist(playlist_name):
        data = request.get_json()
        song_name = data.get('song_name')

        if playlist_name not in playlists :
            return jsonify({"message": "Playlist doesn't exists"}), 404
        if song_name not in songs :
            return jsonify({"message": "Song doesn't exists"}), 404
        playlist = playlists[playlist_name]
        playlist.add_song(songs[song_name])
        return jsonify({"message": "Song added to playlist successfully."}), 201

@app.route('/playlists', methods=['GET'])
def get_playlist():
    return jsonify({"playlists": list(playlists.keys())}), 200


@app.route('/songs', methods=['GET'])
def get_songs():
    return jsonify({"songs": list(songs.keys())}), 200
        
@app.route('/songs/<string:song_name>', methods=['GET'])
def get_one_song(song_name):
        if song_name not in songs:
            return jsonify({"message": "Song doesn't exists"}), 404
        song = songs[song_name]
        formatted_song = {
            "title": song.title,
            "artist": song.artist,
            "genre": song.genre
        }
        return jsonify(formatted_song), 200

@app.route('/playlists/<string:playlist_name>', methods=['GET'])
def get_one_playlist(playlist_name):
        if playlist_name not in playlists:
            return jsonify({"message": "Song doesn't exists"}), 404
        playlist = playlists[playlist_name]
        formatted_playlist = {
            "playlist_title": playlist.name
        }
        return jsonify(formatted_playlist), 200


        
@app.route('/songs/<string:song_name>', methods=['DELETE'])
def delete_songs(song_name):
        data = request.get_json()
        if song_name not in songs:
            return jsonify({"message": "Song doesn't exists"}), 404
        del songs[song_name]
        return jsonify({"message": "Song deleted successfully"}), 201

@app.route('/playlists/<string:playlist_name>/remove-song', methods=['DELETE'])
def delete_song_from_playlist(playlist_name):
    try:
        song_name = request.args.get("songName")
        if playlist_name not in playlists:
            return jsonify({"message": "Playlist doesn't exists"}), 404

        playlist = playlists[playlist_name]
        playlist.delete_song(song_name) 
        return jsonify({"message": "Song Deleted from Playlist Successfully!"}), 201
    except:
        return jsonify({"message": "Song Doesn't Exist in Playlist!"}), 404
       


if __name__ == '__main__':
    app.run(debug=True)