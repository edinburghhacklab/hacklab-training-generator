#!/usr/bin/env python3

import os
from syllabus_processor import SyllabusProcessor

SYLLABUS_FILENAME = 'syllabus.md'

syllabuses = {}

def add_syllabus(result, relpath):
    folders = splitpath(relpath)

    # TODO: store tex to temp files, compile to pdf, move to web dir & record resulting filenames in this dict instead
    nested_set(syllabuses, folders, result)

def generate(path):
    for root, dirs, files in os.walk(path):
        relpath = os.path.relpath(root, path)
        if SYLLABUS_FILENAME in files:
            dirs.clear()

            sp = SyllabusProcessor(root)
            result = sp.generate()
            if result.success:
                add_syllabus(result, relpath)

    # TODO: pass this dict to jinja to build some HTML listing of syllabuses
    print(syllabuses)

def nested_set(dic, keys, value):
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value

def splitpath(path):
    folders = []
    while True:
        path, folder = os.path.split(path)
        if folder != '':
            folders.append(folder)
        else:
            if path != '':
                folders.append(path)
            break
    folders.reverse()
    return folders

if __name__ == "__main__":
    generate('../hacklab-training/syllabuses')
