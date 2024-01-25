'''Резервная копия директории DevStudio.'''
import os
from shutil import copy2
from models import connect
from datetime import datetime


class BackupFile():
    def create_file(self):
        path_split = connect.path_to_devstudio.split('\\')
        path_split.remove(path_split[len(path_split) - 1])
        new_path_backup = '\\'.join(path_split)
        path_dir = f'{new_path_backup}\\backup'

        rw_sign = connect.path_to_devstudio_omx.replace('.omx', '')
        name_file = rw_sign.split("\\")
        new_name = f'{name_file[len(name_file) - 1]}_{datetime.now().strftime("%Y_%m_%d_%H-%M")}'

        if not os.path.isdir(path_dir):
            os.mkdir(path_dir)
        copy2(connect.path_to_devstudio_omx, f'{path_dir}\{new_name}.omx')