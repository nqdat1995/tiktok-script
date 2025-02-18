class DownloadYoutubeOption:
    def __init__(self, channel_id: str, video_type: str, is_get_most_view: bool, view_num: int):
        self.channel_id = channel_id
        self.video_type = video_type
        self.is_get_most_view = is_get_most_view
        self.view_num = view_num