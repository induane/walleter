import os
import logging
import mimetypes
from walleter.utils.text import file_to_list

LOG = logging.getLogger(__name__)
FOLDER = os.path.abspath(os.path.dirname(__file__))

data_files = []
for file in os.listdir(FOLDER):
    mime = mimetypes.guess_type(file)[0]
    if mime in (None, 'text/plain', 'text/markdown', ):
        data_files.append(os.path.join(FOLDER, file))


from walleter.utils.text import file_iter

all_data_iter = file_iter(os.path.join(FOLDER, 'known'))

__all__ = ('all_data', 'data_files', )
