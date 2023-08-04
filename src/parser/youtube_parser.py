import os
import pandas as pd
from googleapiclient.discovery import build

from src.parser.parser import Parser
from src.logger.logger import Logger

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class YouTubeParser(Parser):
    def __init__(self, api_key: str):
        """
        Constructor of the YouTube Parser class.
        Args:
            api_key (str): API key for accessing the YouTube API.
        """
        self.LOG_FILE_NAME = 'youtube_parser.log'
        self.YOUTUBE_API_PARTS = 'snippet,statistics'
        self.YOUTUBE_API_MAX_RESULTS = 50

        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.logger = Logger(self.LOG_FILE_NAME)

    def parse_playlist(self, playlist_id: str) -> pd.DataFrame:
        """
        Parsing information about videos in the playlist
        Args:
            playlist_id (str):  A list of video IDs to retrieve data for.
        Returns:
            pandas.DataFrame: A DataFrame containing the following columns:
                video_id (str): Video ID.
                title (str): The title of the video.
                published_at (str): The date and time the video was published.
                view_count (int): The number of views the video has received.
                like_count (int): The number of likes the video has received.
                comment_count (int): The number of comments the video has received.
                description (str):
        """
        try:
            video_info = self._get_playlist_videos(playlist_id)
            if video_info:
                video_data = self.create_video_dataframe(video_info)
                return video_data
            else:
                return None

        except Exception as e:
            self.logger.log_error(f"An error occurred while parsing the playlist: {str(e)}")
            return None

    def parse_video(self, video_id: str) -> pd.DataFrame:
        """
        Parsing information about video
        Args:
            video_id (str):  video ID to retrieve data for.
        Returns:
            pandas.DataFrame: A DataFrame containing the following columns:
                video_id (str): Video ID.
                title (str): The title of the video.
                published_at (str): The date and time the video was published.
                view_count (int): The number of views the video has received.
                like_count (int): The number of likes the video has received.
                comment_count (int): The number of comments the video has received.
                description (str):
        """
        try:
            video_info = self._get_video_info([video_id])
            if video_info:
                video_data = self.create_video_dataframe(video_info)
                return video_data
            else:
                return None

        except Exception as e:
            self.logger.log_error(f"An error occurred while parsing the video: {str(e)}")
            return None

    def _get_playlist_videos(self, playlist_id: str) -> list:
        """
        Retrieves video information from YouTube API.
        Args:
            playlist_id: Playlist IDs to retrieve data for.
        Returns:
            list: A list of dictionaries containing video information.
        """
        try:
            request = self.youtube.playlistItems().list(
                part='contentDetails',
                playlistId=playlist_id,
                maxResults=self.YOUTUBE_API_MAX_RESULTS
            )

            video_info = []
            while request:
                response = request.execute()
                items = response.get('items', [])
                video_ids = [item['contentDetails']['videoId'] for item in items]
                video_info.extend(self._get_video_info(video_ids))
                request = self.youtube.playlistItems().list_next(request, response)

            return video_info

        except Exception as e:
            self.logger.log_error(f"An error occurred while retrieving playlist videos: {str(e)}")
            return None

    def _get_video_info(self, video_ids: list[str]) -> list:
        """
        Retrieves video information from YouTube API.
        Args:
            video_ids: A list of video IDs to retrieve data for.
        Returns:
            list: A list of dictionaries containing video information.
        """
        try:
            # Execute the request for each chunk of video IDs
            response = self.youtube.videos().list(
                part=self.YOUTUBE_API_PARTS,
                id=','.join(video_ids)  # Combine video IDs into a comma-separated string
            ).execute()

            return response['items']

        except Exception as e:
            self.logger.log_error(f"An error occurred while retrieving video information: {str(e)}")
            return None

    @staticmethod
    def create_video_dataframe(video_info: list) -> pd.DataFrame:
        """
        Creates a Pandas DataFrame from the video information list.
        Args:
            video_info: A list of dictionaries containing video information.
        Returns:
            pandas.DataFrame: A DataFrame containing video data.
        """
        data = {
            'video_id': [info['id'] for info in video_info],
            'title': [info['snippet']['title'] for info in video_info],
            'published_at': [info['snippet']['publishedAt'] for info in video_info],
            'view_count': [info['statistics']['viewCount'] for info in video_info],
            'like_count': [info['statistics']['likeCount'] for info in video_info],
            'comment_count': [info['statistics']['commentCount'] for info in video_info],
            'description': [info['snippet']['description'] for info in video_info]
        }
        video_data = pd.DataFrame(data)

        return video_data


if __name__ == "__main__":
    api_key = os.environ['API_KEY']
    playlist_id = "PLcQngyvNgfmK0mOFKfVdi2RNiaJTfuL5e"
    parser = YouTubeParser(api_key)

    output_file = os.path.join(BASE_DIR, 'data', 'raw_data', 'info_overclocking.csv')
    video_info = parser.parse_playlist(playlist_id)
    if video_info is not None:
        video_info.to_csv(output_file, index=False)
