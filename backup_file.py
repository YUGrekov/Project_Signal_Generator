'''Резервная копия директории DevStudio.'''
import os
from shutil import copytree
from shutil import rmtree
from models import connect


class BackupFile():
    def create_file(self):
        new_path_backup = connect.path_to_devstudio.replace('typical_prj', '')
        path_dir = f'{new_path_backup}\\backup'

        if os.path.isdir(path_dir):
            rmtree(path_dir)
        copytree(connect.path_to_devstudio, path_dir)
