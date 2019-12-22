import os
import re
import subprocess


newline = '\n'
recipe_directory = os.path.join(os.path.dirname(__file__), 'recipes')

for path in [os.path.join(recipe_directory, x) for x in os.listdir(recipe_directory)
             if x.endswith('.md') and not x.startswith('print_')]:
    new_rows = []
    date = None
    title = None

    with open(path) as fid:
        for row in fid:
            if not row.startswith(('<div', '</div', '  <a', '<br')):
                date_match = re.match(r'^<p align="right">(.+)</p>.*', row)
                title_match = re.match(r'^<h1 align="center">(.+)</h1>.*', row)

                # print(os.path.basename(path), bool(date_match), bool(title_match), row.strip())

                if date_match:
                    date = date_match.group(1)
                elif title_match:
                    title = title_match.group(1)
                else:
                    new_rows.append(row)

    if date and title:
        final_rows = ['# ' + title + newline, date + newline] + new_rows
        directory, basename = os.path.split(path)
        basename = 'print_' + basename

        with open(os.path.join(directory, basename), 'w') as oid:
            oid.write(''.join(final_rows))

    else:
        raise RuntimeError('Could not find date and title ...')


all_printable_paths = [os.path.join(recipe_directory, x) for x in os.listdir(recipe_directory) if x.startswith('print_')]
compile_command = (f'pandoc -s '
                   f'-V geometry:margin=1.5in '
                   f'--toc --toc-depth=1 '
                   f'--include-in-header titlesec.tex '
                   f'-o recipe-book.pdf {" ".join(all_printable_paths)}')

subprocess.call(compile_command, shell=True)
[os.remove(os.path.join(recipe_directory, x)) for x in os.listdir(recipe_directory) if x.startswith('print_')]

print('complete.')

