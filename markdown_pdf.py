#!/usr/bin/env python
from __future__ import print_function

import os

import grip
import pdfkit

recipe_name = 'aloo-gobi.md'
html_directory = 'html'
pdf_directory = 'pdf'

recipe_input = os.path.join('recipes', recipe_name)

html_output = os.path.join(html_directory, recipe_name + '.html')
pdf_output = os.path.join(pdf_directory, recipe_name + '.pdf')

grip.export(path=recipe_input, out_filename=html_output)
pdfkit.from_file(html_output, pdf_output)