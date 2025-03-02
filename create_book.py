import datetime
import os
import re
import subprocess

TIME_ORDER: bool = False  # if not time ordered, goes alphabetical
NEWLINE = '\n'
RECIPE_DIRECTORY = os.path.join(os.path.dirname(__file__), 'recipes')
OVERRIDE_DIRECTORY = os.path.join(os.path.dirname(__file__), '2025')  # None
RECIPE_DIRECTORY = RECIPE_DIRECTORY if not OVERRIDE_DIRECTORY else OVERRIDE_DIRECTORY
REMOVE_DATES: bool = True

for path in [os.path.join(RECIPE_DIRECTORY, x) for x in os.listdir(RECIPE_DIRECTORY)
             if x.endswith('.md') and not x.startswith('print_')]:
    new_rows = []
    date = 'meh' # None
    title = None

    with open(path) as fid:
        for row in fid:
            if not row.startswith(('<div', '</div', '  <a', '<br')):
                date_match = re.match(r'^<p align="right">(.+)</p>.*', row)
                title_match = re.match(r'^<h1 align="center">(.+)</h1>.*', row)

                # print(os.path.basename(path), bool(date_match), bool(title_match), row.strip())

                if date_match:
                    date = date_match.group(1)
                    date_obj = datetime.datetime.strptime(date, '%m.%d.%Y')
                elif title_match:
                    title = title_match.group(1)
                else:
                    new_rows.append(row.strip() + NEWLINE)

    if date and title:

        if REMOVE_DATES:
            final_rows = ['# ' + title + NEWLINE] + new_rows
        else:
            final_rows = ['# ' + title + NEWLINE, date + NEWLINE] + new_rows

        directory, basename = os.path.split(path)

        basename = f'print_{date_obj.strftime("%Y%m%d")}_{basename}' if TIME_ORDER else f'print_{basename}'

        with open(os.path.join(directory, basename), 'w') as oid:
            oid.write(''.join(final_rows))

    else:
        raise RuntimeError('Could not find date and title ...')


all_printable_paths = sorted(
    [os.path.join(RECIPE_DIRECTORY, x) for x in os.listdir(RECIPE_DIRECTORY) if x.startswith('print_')]
)

compile_command = (f'/opt/homebrew/bin/pandoc -s '
                   f'-V geometry:margin=1.5in '
                   f'--toc --toc-depth=1 '
                   f'--pdf-engine="/Library/TeX/texbin/pdflatex" '
                   f'--include-in-header titlesec.tex '
                   f'-o recipe-book.pdf {" ".join(all_printable_paths)}')

subprocess.call(compile_command, shell=True)
[os.remove(os.path.join(RECIPE_DIRECTORY, x)) for x in os.listdir(RECIPE_DIRECTORY) if x.startswith('print_')]

print('complete.')

