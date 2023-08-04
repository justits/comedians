from abc import ABC, abstractmethod
import pandas as pd
from datetime import datetime


class BaseProcessor(ABC):
    def __init__(self, video_data: pd.DataFrame):
        if not isinstance(video_data, pd.DataFrame):
            raise ValueError("video_data must be a DataFrame")
        self.video_data = video_data

    def process_data(self) -> pd.DataFrame:
        processed_data = self._common_data_processing()
        processed_data['link'] = self._create_link()
        processed_data['show_id'] = self._get_show_id()
        processed_data['comedians'] = self._definition_of_comedians()
        return processed_data

    def _common_data_processing(self) -> pd.DataFrame:
        columns = ['title', 'published_at', 'view_count', 'like_count', 'comment_count']
        processed_data = self.video_data[columns].copy()
        processed_data['published_at'] = pd.to_datetime(processed_data['published_at'])
        processed_data['update_at'] = pd.Timestamp(datetime.now())
        return processed_data

    @abstractmethod
    def _create_link(self) -> pd.Series:
        pass

    @abstractmethod
    def _get_show_id(self) -> str:
        pass

    @abstractmethod
    def _get_comedians_list(self) -> pd.Series:
        pass
