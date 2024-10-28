from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect




app = Flask(__name__)
CORS(app)
csrf = CSRFProtect(app)
playlists = {}

class Song:
    def __init__(self, title, artist, genre):
        self.title = title
        self.artist = artist
        self.genre = genre
    
    def __str__(self):
        return f"{self.title} by {self.artist} and genre is {self.genre}"
    
class Node:
    def __init__(self, song):
        self.song = song
        self.next = None
        self.prev = None

class Playlist:
    def __init__(self, name):
        self.name = name
        self.head = None
        self.prev = None


    def add_song(self, song):
        new_node = Node(song)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
    # def __init__(self):
    #     self.head = None
    #     self.tail = None

    # def add_song(self, title, artist, genre):
    #     new_song = Song(title, artist, genre)
    #     new_node = Node(new_song)
    #     if not self.head:
    #         self.head = new_node
    #         self.tail = new_node
    #     else:
    #         self.tail.next = new_node
    #         new_node.prev = self.tail
    #         self.tail = new_node
    
    def delete_song(self, title):
        current = self.head
        while current:
            if current.song.title == title:
                if current == self.head:
                    self.head = current.next
                if current == self.tail:
                    self.tail = current.prev
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
            songs.append(str(current.song))
            current = current.next
        return songs

    # def traverse_playlist(self):
    #     if not self.head:
    #         print("Playlist is empty.")
    #         return
    #     current = self.head
    #     while current:
    #         print(f"Title: {current.song.title}")
    #         print(f"Artist: {current.song.artist}")
    #         print(f"Genre: {current.song.genre}")
    #         print("------------------------------")
    #         current = current.next

@csrf.exempt
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        playlist_name = data.get('playlist_name')
        song_title = data.get['song_title']
        song_artist = data.get['song_artist']
        song_genre = data.get['song_genre']

        if playlist_name not in playlists:
            playlists[playlist_name] = Playlist(playlist_name)
            print("Created a new playlist")

        playlist = playlists[playlist_name]
        playlist.add_song(Song(song_title, song_artist, song_genre))
        return jsonify({"message": "Song added successfully."}), 201
    return jsonify({"message": "Index working"}), 200

if __name__ == '__main__':
    app.run(debug=True)

# playlist_manager = Playlist()

# playlist_manager.add_song("Shape of You", "Ed Sheeran", "Pop")
# playlist_manager.add_song("Someone Like You", "Adele", "Pop")
# playlist_manager.add_song("Bohemian Rhapsody", "Queen", "Rock")

# playlist_manager.delete_song("Someone Like You")

# playlist_manager.traverse_playlist()
