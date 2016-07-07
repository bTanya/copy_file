from multiprocessing import Pool
import os
import shutil
from functools import partial
import json

def get_settings(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        entry = json.load(f)
        f.close()
    return entry['threads_number']

def copy_file(src, dst, file):
    print(file)
    src_path = src + file
    dst_path = dst + file
    print(src_path)
    print(dst_path)
    if os.path.isdir(src_path):
        print("dir " + file + "  :copy started")
        copy_dir(src_path, dst_path)
        print("dir " + file + "  :copy completed")
    else:
        print(file + "  :copy started")
        shutil.copyfile(src_path, dst_path)
        print(file + "  :copy completed")

def copy_dir(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        print("s:   "+s)
        d = os.path.join(dst, item)
        print("d:   "+d)
        if os.path.isdir(s):
            if not os.path.exists(d):
                os.makedirs(d)
            copy_dir(s, d, symlinks, ignore)
        else:
            shutil.copyfile(s, d)

def get_files_path():
    src_path = input('Введите путь к каталогу из которого '
                      'нужно скопировать файлы: ')
    dst_path = input('Введите путь к каталогу, в который '
                    'нужно скопировать файлы: ')
    if os.path.exists(src_path) and os.path.exists(dst_path):
        return src_path, dst_path
    else:
        print('Неверный путь.')
    return get_files_path()

if __name__ == '__main__':

    src_path,dst_path = get_files_path()
    files = os.listdir(src_path)
    threads_number = get_settings('settings.json')
    if not threads_number:
        threads_number = 3
    pool = Pool(threads_number)
    pool.map(partial(copy_file,src_path, dst_path), files)
    pool.close()
