import logging

from uuid import uuid4
from os.path import join, stat, exists
from os import remove
from shutil import move

from app import cfg
from .file_storage_exceptions import (FileExtensionError, FileMimeTypeError,
                                        FileSizeLimitError, FileNotFoundError)

_file_set = cfg.FILE_UPLOADS.FILE_SETS['REPORT']

def save(file):
    file_extension = file.filename.rsplit('.', 1)[1].lower()

    if file_extension not in _file_set['ALLOWED_EXTENSIONS']:
        raise FileExtensionError
    if file.mimetype not in _file_set['ALLOWED_MIME_TYPES']:
        raise FileMimeTypeError
    if file.content_length > _file_set['MAX_SIZE']: # Не будет работать, пока Chrome и Firefox не перестанут ставить Content-Length равным 0 ¯\_(ツ)_/¯
        raise FileSizeLimitError

    filename = str(uuid4())
    tmp_path = join(cfg.FILE_UPLOADS.TEMP_FOLDER, filename)
    file.save(tmp_path)
    size = stat(tmp_path).st_size
    logging.debug('File size is {}'.format(size))
    if size > _file_set.MAX_SIZE:
        remove(tmp_path)
        raise FileSizeLimitError
    new_path = join(_file_set.FOLDER, filename)
    move(tmp_path, new_path)
    return filename

def get(id):
    return _file_set.FOLDER, id

def remove(filename):
    path = join(_file_set.FOLDER, filename)
    if exists(path):
        remove(path)
    else:
        raise FileNotFoundError