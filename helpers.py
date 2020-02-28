from datetime import datetime
from my_vk_api import unknown_url
from my_vk_api import unknown_title
from my_vk_api import unknown_artist


def to_datetime(unix_time):
    return datetime.utcfromtimestamp(unix_time).strftime('%d-%m-%Y %H:%M:%S')


def char_offset(c, offset):
    return chr(ord(c) + offset)


def row_range(start_column, start_row, size):
    return start_column + str(start_row) + ":" + char_offset(start_column, size) + str(start_row)


def square_range(start_column, start_row, size_column, size_row):
    return start_column + str(start_row) + ":" + char_offset(start_column, size_column) + str(start_row + size_row)


photo_sizes = ['w', 'z', 'y', 'r', 'q', 'p', 'o', 'x', 'm', 's']


# def inline_url(url):
#     return "<a href='" + url + "'>'" + url + "'</a>"


def photo_to_url(attachment):
    sizes = attachment['photo']['sizes']

    sizes_dict = {}

    for s in sizes:
        sizes_dict[s['type']] = s['url']

    for s in photo_sizes:
        img_url = sizes_dict.get(s, None)

        if img_url is not None:
            return img_url

    return unknown_url


def audio_to_str(attachment):
    audio = attachment['audio']

    try:
        artist = audio['artist']
    except KeyError:
        artist = unknown_artist

    try:
        title = audio['title']
    except KeyError:
        title = unknown_title

    return '"' + artist + ' - ' + title + '"'


def doc_to_url(attachment):
    doc = attachment['doc']

    try:
        return doc['url']
    except KeyError:
        return unknown_url

#
# def vk_video_to_str(video):
#     return '==='
#
#
# def youtube_to_str(video):
#
#
#     return "---"
#
#
# video_platforms = {'YouTube': youtube_to_url}


def video_to_str(attachment):
    video = attachment['video']

    try:
        platform = video['platform']
    except KeyError:
        platform = 'VK'
    try:
        title = video['title']
    except KeyError:
        title = unknown_title

    return platform + ' "' + title + '"'

    # try:
    #     return video_platforms[platform](video)
    # except KeyError:
    #     return '<UNKNOWN VIDEO PLATFORM>'
