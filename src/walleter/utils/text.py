"""Text tools."""
# Standard
import logging
import string

LOG = logging.getLogger(__name__)
STRIP = ('\r\n', '\n', '\t', ' ')


def clean(value):
    """Clean special characters from a string."""
    return ''.join([x.strip() for x in value])


def file_to_list(path):
    """Given a file return all words lowercased in an array."""
    data = []
    with open(path, 'rb') as f:
        for row in f.readlines():
            row = row.replace('\r\n', ' ').replace('\n', ' ').strip()
            row_words = row.split(' ')
            new_row = []
            for item in row_words:
                cleaned_data = clean(item)
                if cleaned_data:
                    new_row.append(cleaned_data)
            data.extend(new_row)
    LOG.debug(str(data))
    return data


def file_iter(path):
    with open(path, 'rb') as f:
        for row in f.readlines():
            for r in STRIP:
                row = row.strip(r)
                yield row
