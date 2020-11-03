import json
import os
from datetime import datetime

from config import settings

def write_log(line):
    """
    write in log
    """
    dir_file = os.path.join(settings.BASE_DIR, 'log')
    try:
        with open(dir_file, mode='a') as f:
            f.writelines('[{}]: '.format(datetime.now().strftime('%d/%m/%Y %H:%M:%S')) + line + '\n')
    except Exception:
        pass

def read_json_file_convert_to_python(abs_dir):
    """
    read the json file and converter to python
    """
    try:
        with open(abs_dir) as f:
            data = json.load(f)
            return data
    except Exception:
        write_log("Error read or converter json file to python")
        return []

