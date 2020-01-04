# # Move rendered book files into `/doc` directory
# !NOT WORKING
# 
# dir.create('../docs')
# 
# files <- list.files('_book')
# files <- str_c('_book/', files)
# 
# file.copy(from = files, 
#           to = '../docs', overwrite = TRUE)
