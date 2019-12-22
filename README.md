# Markdown Recipe Book
*A living cookbook written in markdown that is easily compiled to PDF*

## Setup
Assuming OS X operating system:
- `python` executable should refer to Python3
- Install pandoc -- `brew install pandoc`
- Install MacTex -- `brew cask install mactex`

## Create Book
`python create_book.py` uses the markdown files in `./recipes` (ignores `./development` where recipes in
development live) and the `titlesec.tex` LaTex file as input.  Outputs an updated `recipe-book.pdf` file.

Book can be viewed in GitHub [here](/recipe-book.pdf)
