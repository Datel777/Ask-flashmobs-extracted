import requests

# I hide my secret access toke in file
vkAccessTokenFile = open("vkAccessToken", "r")

vk_main_params = {
    "lang": 0,
    "access_token": vkAccessTokenFile.readline(),
    "v": "5.92"
}

vkAccessTokenFile.close()
del vkAccessTokenFile

vk_query_limit = 100
vk_query_base = 'https://api.vk.com/method/'
# vk_ats = {
#     'photo' : lambda ()
# }

# default strings for unknown data
unknown_url = '<UNKNOWN URL>'
unknown_artist = '<UNKNOWN ARTIST>'
unknown_title = '<UNKNOWN TITLE>'


def get_board_comments_iter(params, offset):
    params["offset"] = offset
    return [requests.get(vk_query_base + 'board.getComments', params).json()['response'],
            offset + vk_query_limit]


def get_board_comment_n(group_id, topic_id, n):
    all_params = {
        **vk_main_params,
        "group_id": group_id,
        "topic_id": topic_id,
        "count": 1,
        "offset": n
    }

    result = requests.get(vk_query_base + 'board.getComments', all_params).json()['response']["items"]

    if not result:
        return None

    return result[0]


def get_board_comments_first_n(group_id, topic_id, n):
    all_params = {
        **vk_main_params,
        "group_id": group_id,
        "topic_id": topic_id,
        'photo_sizes': 1,
        "count": n
    }

    return requests.get(vk_query_base + 'board.getComments', all_params).json()['response']["items"]


def get_board_comments(group_id, topic_id):
    offset = 0

    all_params = {
        **vk_main_params,
        "group_id": group_id,
        "topic_id": topic_id,
        "count": vk_query_limit,
        "offset": 0
    }

    [response, offset] = get_board_comments_iter(all_params, offset)
    count = response["count"]

    items = response["items"]

    while offset < count:
        [response, offset] = get_board_comments_iter(all_params, offset)
        items += response["items"]

    return items
