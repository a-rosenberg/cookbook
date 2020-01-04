# Process .md files

## move md files over into a tmp directory in `/book`

library(tidyverse)

f <- list.files('../recipes')
f <- f[stringr::str_detect(f, ".md")]
fo <- str_c('../recipes/', f)

ff <- stringr::str_sub(f, end = -4)
ff <- stringr::str_c(1:length(ff), "-", ff, ".Rmd")

dir.create('tmp')

ff <- str_c('tmp/', ff)

file.copy(from = fo, to = ff)

## add necessary level-1 headers to md files in `/book`

add_correct_header <- function(file) {
  lines_of_file <- read_lines(file)
  split_names <- str_split(file, "-")
  split_names <- split_names[[1]][-1]
  l1_header <- str_c(split_names, collapse = " ")
  l1_header <- str_sub(l1_header, end = -5)
  l1_header <- str_c("# ", l1_header)
  lines_of_file <- append(lines_of_file, l1_header, after = 10)
  write_lines(lines_of_file, file)
}

ff %>% 
  map(add_correct_header)
