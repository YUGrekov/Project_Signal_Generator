'''Резервная копия директории DevStudio.'''
import os
from shutil import copytree
from shutil import rmtree
from models import connect


class BackupFile():
    def create_file(self):
        path_split = connect.path_to_devstudio.split('\\')
        path_split.remove(path_split[len(path_split) - 1])

        new_path_backup = '\\'.join(path_split)
        path_dir = f'{new_path_backup}\\backup'

        if os.path.isdir(path_dir):
            rmtree(path_dir)
        copytree(connect.path_to_devstudio, path_dir)