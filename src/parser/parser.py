from abc import ABC, abstractmethod


class Parser(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def parse_video(self, video_id:str):
        pass

    @abstractmethod
    def parse_playlist(self, playlist_id: str):
        pass

