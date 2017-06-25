#!/usr/bin/env python3

import jinja2
import os
import subprocess
from syllabus_processor import SyllabusProcessor
import sys
from tempfile import NamedTemporaryFile

SYLLABUS_FILENAME = 'syllabus.md'

syllabuses = {}

class Syllabus:
    def __init__(self, name):
        self.name = name
        self.files = {}

def add_syllabus(result, relpath, output_dir):
    folders = splitpath(relpath)
    s = Syllabus(folders[-1])
    dest = os.path.join(output_dir, relpath)
    os.makedirs(dest, exist_ok=True)

    training_card_filename = '{}-training-card.pdf'.format(folders[-1].replace(' ', '-'))
    s.files[s.name + ' training card'] = os.path.join(relpath, training_card_filename)
    compile_tex(result.card, os.path.join(dest, training_card_filename))

    training_doc_filename = '{}-training-doc.pdf'.format(folders[-1].replace(' ', '-'))
    s.files[s.name + ' training doc'] = os.path.join(relpath, training_doc_filename)
    compile_tex(result.doc, os.path.join(dest, training_doc_filename))

    nested_set(syllabuses, folders, s)

def compile_tex(tex_string, destination_filename):
    # TODO: create a whole temp directory so we can cleanup after pdflatex
    with NamedTemporaryFile('w', encoding='utf-8') as f:
        f.write(tex_string)
        f.flush()
        for i in range(5):
            output = subprocess.check_output(['pdflatex', '-jobname='+os.path.splitext(destination_filename)[0], f.name])
            if not 'Rerun LaTeX' in str(output):
                break

def generate(syallabus_dir, output_dir):
    for root, dirs, files in os.walk(syallabus_dir):
        relpath = os.path.relpath(root, syallabus_dir)
        if SYLLABUS_FILENAME in files:
            dirs.clear()

            sp = SyllabusProcessor(root)
            result = sp.generate()
            if result.success:
                add_syllabus(result, relpath, output_dir)

    env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.abspath('.')), extensions=['jinja2.ext.do'])
    site_template = env.get_template('training-site.tmpl')
    with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(site_template.render(syllabuses = syllabuses))

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
    if len(sys.argv) < 3:
        print("Usage: {} <syllabus_dir> <output_dir>".format(sys.argv[0]))
        sys.exit()
    generate(sys.argv[1], sys.argv[2])
