from my_vk_api import get_board_comments
from my_vk_api import get_board_comment_n
from my_vk_api import get_board_comments_first_n

from my_google_excel_api import google_client
from helpers import *

# Main config for this script
google_sheet = google_client.open('Ask flashmobs extracted').sheet1
vk_group_id = 60424693
vk_topic_id = 29620642

headers = ['Краткое описание', 'url', 'Дата', 'Текст', 'Приложения', 'Теги']
attr_column = {'id': 2, 'date': 3, 'text': 4, 'attachments': 5}
url_base = 'vk.com/topic-'

attach_func = {'photo': photo_to_url, 'audio': audio_to_str, 'doc': doc_to_url, 'video': video_to_str}

# find cells by regular expressions
# amount_re = re.compile(r'(Big|Enormous) dough')
# cell = worksheet.findall(amount_re)


def id_to_url(post_id):
    return url_base + str(vk_group_id) + '_' + str(vk_topic_id) + '?post=' + str(post_id)


def attachment_to_str(attachment):
    attachment_type = attachment['type']
    text = '[' + attachment_type + '] '

    # debug = attach_func
    # debug_func = attach_func['video']

    try:
        text += attach_func[attachment_type](attachment)
    except KeyError:
        text += '<UNKNOWN FUNCTION FOR TYPE>'

    return text


def attachments_to_str(attachments):
    return_lists = []
    for attachment in attachments:
        return_lists.append(attachment_to_str(attachment))

    return '\n'.join(return_lists)


attr_func = {'id': id_to_url, 'date': to_datetime, 'attachments': attachments_to_str}


def init_sheet():
    cells = google_sheet.range(1, 1, 1, 1 + len(headers) - 1)

    for i, cell in enumerate(cells):
        cell.value = headers[i]

    google_sheet.update_cells(cells)


def commit_items(items):
    start_column = 2  # 'B'
    start_row = 2
    column_count = 4  # to 'E'
    row_count = len(items)
    cells = google_sheet.range(start_row, start_column, start_row+row_count, start_column+column_count-1)

    for i, attributes in enumerate(items):
        for attr, val in attributes.items():
            try:
                column = attr_column[attr]
                cell = cells[i*column_count + column - start_column]

                try:
                    cell.value = attr_func[attr](val)
                except KeyError:
                    cell.value = val
            except KeyError:
                pass

    google_sheet.update_cells(cells)


# print(google_sheet.cell(1, 1).value)  # Test google sheet
# init_sheet()  # Creating  headers
# comments = get_board_comments(vk_group_id, vk_topic_id)  # Getting all comments
comments = get_board_comments_first_n(vk_group_id, vk_topic_id, 10)  # Getting first 100 comments
# commit_items(comments)   # Commit data to google sheet

print(comments)  # Debug comments


