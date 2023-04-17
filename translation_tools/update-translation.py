#!/usr/bin/env python
# coding=utf-8

"""
This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.
"""
from libopensesame.py3compat import *
import yaml
import re
import os
import sys
import subprocess
import argparse

EXCLUDE_FOLDERS = ['build', 'dist', 'deb_dist', 'pgs4a-0.9.4']
LUPDATE = ['pylupdate5']  # + ['-noobsolete']
LRELEASE = 'lrelease'
TRANSLATABLES_PY = os.path.abspath('translation_tools/translatables.py')
TRANSLATE_PRO = os.path.abspath('translation_tools/translate.pro')
LOCALES = [
    'fr_FR',
    'de_DE',
    'it_IT',
    'zh_CN',
    'ru_R',
    'es_ES',
    'ja_JP',
    'tr_TR',
    'translatables'
]
pro_tmpl = '''FORMS = {ui_list}
SOURCES = {sources}
TRANSLATIONS = {locales}
CODECFORTR = UTF-8
CODECFORSRC = UTF-8
'''


class Translatables(object):

    def __init__(self):

        self._translatables = {}

    def add(self, context, translatable):

        if context not in self._translatables:
            self._translatables[context] = set()
        self._translatables[context].add(safe_decode(translatable))

    def to_file(self, path=TRANSLATABLES_PY):

        with open(path, 'w') as fd:
            fd.write(str(self))

    def __str__(self):

        ls = []
        for context, translatables in self._translatables.items():
            ls.append('class %s:\n\tdef _():' % context)
            for s in translatables:
                # Escape all unescapted single quotes
                s = re.sub(r"(?<!\\)'", "\\'", s)
                s = s.replace('\n', '\\n')
                ls.append('\t\tself.tr(\'%s\')' % s)
        return safe_str('\n'.join(ls) + '\n')


def parse_py(path, t):

    print(path)
    re_context = r'_ = translation_context\(u?[\'"](?P<name>\w+)[\'"], category=u?[\'"](?P<category>\w+)[\'"]\)'
    re_translatable = r'\b_\(u?(?P<quote>[\'"])(?P<translatable>.+?)(?P=quote)\)'
    with open(path) as fd:
        src = safe_decode(fd.read())
        if '\nfrom libqtopensesame.misc import _' in src:
            raise Exception('Deprecated translation in %s' % path)
        m = re.search(re_context, src)
        if m is None:
            print('\tcontext: None')
            return
        context = '%s_%s' % (m.group('category'), m.group('name'))
        print('\tcontext: %s' % context)
        m = re.findall(re_translatable, src)
        for quotes, s in m:
            print('\ttranslatable: %s' % s)
            t.add(context, s)
        print('\t%d translatables' % len(m))


def parse_yaml(path, t, category):

    print(path)
    if category == 'auto':
        folder = os.path.basename(os.path.dirname(os.path.dirname(path)))
        print(folder)
        if folder == 'opensesame_extensions':
            category = 'extension'
        elif folder == 'opensesame_plugins':
            category = 'plugin'
        else:
            raise ValueError('Unkown category for %s' % path)
    name = os.path.basename(os.path.dirname(path))
    context = '%s_%s' % (category, name)
    print('\tcontext: %s' % context)
    with open(path) as fd:
        s = fd.read().replace('\t', '    ')
        d = yaml.load(s, Loader=yaml.FullLoader)
        for field in ['label', 'description', 'tooltip']:
            if field not in d:
                continue
            t.add(context, d[field])
            print('\ttranslatable: %s' % d[field])
        if 'category' in d:
            t.add('core_item_category', d['category'])
        if 'controls' in d:
            for _d in d['controls']:
                for field in ['label', 'info', 'prefix', 'suffix']:
                    if field not in _d:
                        continue
                    t.add(context, _d[field])
                    print('\ttranslatable: %s' % _d[field])


def parse_folder(path, t, ui_list, category):

    for fname in os.listdir(path):
        _fname = os.path.join(path, fname)
        if fname.endswith('.py'):
            parse_py(_fname, t)
            continue
        if fname in ['info.yaml', 'info.json']:
            parse_yaml(_fname, t, category)
            continue
        if fname.endswith('.ui'):
            ui_list.append(_fname)
            continue
        if (
            os.path.isdir(_fname) and
            os.path.basename(_fname) not in EXCLUDE_FOLDERS
        ):
            parse_folder(_fname, t, ui_list, category)


def ts_path(ts_folder, locale):
    
    return os.path.abspath(os.path.join(ts_folder, locale + '.ts'))


def qm_path(qm_folder, locale):
    
    return os.path.abspath(os.path.join(qm_folder, locale + '.qm'))
                                        

def compile_ts(locales, t, ui_list, ts_folder, fname=TRANSLATE_PRO):

    t.to_file()
    if not os.path.exists(ts_folder):
        print('No ts files found')
        return
    pro = pro_tmpl.format(
        ui_list=' \\\n\t'.join(ui_list),
        locales=' \\\n\t'.join(
            [
                ts_path(ts_folder, locale)
                for locale in locales
                if locale == 'translatables' or os.path.exists(
                    ts_path(ts_folder, locale)
                )
            ]
        ),
        sources=TRANSLATABLES_PY
    )
    with open(fname, 'w') as fd:
        fd.write(pro)
    cmd = LUPDATE + [fname]
    subprocess.call(cmd)


def compile_qm(locales, ts_folder, qm_folder):

    for locale in locales:
        src = ts_path(ts_folder, locale)
        if not os.path.exists(src):
            print('{} does not exist'.format(src))
            continue
        target = qm_path(qm_folder, locale)
        cmd = [LRELEASE, src, '-qm', target]
        subprocess.call(cmd)


def check_markdown_translations(dirname, locale):

    if not os.path.isdir(dirname):
        print('{} is not a directory'.format(dirname))
        return
    for basename in os.listdir(dirname):
        path = os.path.join(dirname, basename)
        if os.path.isdir(path) and basename != 'locale':
            check_markdown_translations(path, locale)
            continue
        if not path.endswith('.md'):
            continue
        if not os.path.exists(
            os.path.join(dirname, 'locale', locale, basename)
        ):
            print('- %s' % path)
            

def list_markdown_translations(dirname):
    
    if not os.path.isdir(dirname):
        print('{} is not a directory'.format(dirname))
        return
    for basename in os.listdir(dirname):
        path = os.path.join(dirname, basename)
        if os.path.isdir(path) and basename != 'locale':
            list_markdown_translations(path)
            continue
        if not path.endswith('.md'):
            continue
        print('- `{}`'.format(path))


def add_message_encoding(locales, ts_folder):

    for locale in locales:
        path = ts_path(ts_folder, locale)
        if not os.path.exists(path):
            print('{} does not exist'.format(path))
            continue
        with open(path) as fd:
            content = safe_decode(fd.read())
            if '<message>' not in content:
                continue
        with open(path, 'w') as fd:
            content = content.replace(
                '<message>',
                '<message encoding="UTF-8">'
            )
            fd.write(safe_str(content))
            print('Adding encoding to message tags for %s' % locale)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Update ts and qm files for OpenSesame-related projects')
    parser.add_argument('--list-markdown',
                        action='store_true',
                        help='Activate to list Markdown tabs and then quit')
    parser.add_argument('--category', type=str, default='auto',
                        choices=['plugin', 'extension', 'auto'],
                        help='Should be "plugin", "extension", or "auto"')
    parser.add_argument('--ts_folder', type=str,
                        default='libqtopensesame/resources/ts',
                        help='The folder that contains the ts files')
    parser.add_argument('--qm_folder', type=str,
                        default='libqtopensesame/resources/locale',
                        help='The folder that contains the qm files')
    args = parser.parse_args()
    if args.list_markdown:
        list_markdown_translations('opensesame_extensions')
        list_markdown_translations('opensesame_plugins')
        list_markdown_translations('libqtopensesame/resources')
        sys.exit()
    translatables = Translatables()
    ui_list = []
    print('Parsing folders …')
    parse_folder(os.path.abspath('.'), translatables, ui_list,
                 category=args.category)
    print('Adding message encodings …')
    add_message_encoding(LOCALES, args.ts_folder)
    print('Compiling ts …')
    compile_ts(LOCALES, translatables, ui_list, args.ts_folder)
    print('Compiling qm …')
    compile_qm(LOCALES, args.ts_folder, args.qm_folder)
    for locale in LOCALES:
        if locale == 'translatables':
            continue
        print('Markdown translations for %s' % locale)
        check_markdown_translations('opensesame_extensions', locale)
        check_markdown_translations('opensesame_plugins', locale)
        check_markdown_translations('openselibqtopensesame/resourcessame_resources', locale)
        print()
 
