import pandas as pd

from src.processor.base_processor import BaseProcessor


class YouTubeProcessor(BaseProcessor):
    def __init__(self, video_data: pd.DataFrame, show_id: str, members_func):
        super().__init__(video_data)
        self.show_id = show_id
        self.members_func = members_func

    def _get_show_id(self) -> str:
        return self.show_id

    def _create_link(self) -> pd.Series:
        return 'https://www.youtube.com/watch?v=' + self.video_data['video_id']

    def _get_comedians_list(self) -> pd.Series:
        return self.video_data.apply(lambda x: self.members_func(x), axis=1)
