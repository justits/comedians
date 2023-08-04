def members_overlocking(x):
    sep = r",| и "
    if x.number > 16:
        members = x.title.split('[')[1].split(']')[0]
    else:
        regex = "Сегодня разгоняли|В этот раз собрались|Сегодня разгоняют|В пилоте снялись"
        start = re.search(regex, x.description).span()[1]
        members = x.description[start:].split('.')[0]
    return [member.strip() for member in re.split(sep, members)]



if __name__ == "__main__":
    api_key = os.environ['API_KEY']
    playlist_id = "PLcQngyvNgfmK0mOFKfVdi2RNiaJTfuL5e"
    parser = YouTubeParser(api_key)

    # Загрузка данных для плейлиста
    playlist_data = youtube_parser.parse_playlist(playlist_id)

    # Обработка данных для плейлиста
    show_id = "overlocking"

    playlist_processor = YouTubeProcessor(playlist_data, show_id, members_overlocking)
    processed_playlist_data = playlist_processor.process_data()
