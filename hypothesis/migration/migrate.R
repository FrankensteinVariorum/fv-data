# This script reads out annotations from the old pghfrankenstein rendering of
# the Thomas edition to relocate them to
# https://frankensteinvariorum.github.io/fv-collation/Frankenstein_Thom.html

library(glue)
library(httr)
library(jsonlite)
library(purrr)
library(progress)
library(stringr)

h_api <- "https://api.hypothes.is/api/annotations"

# Keep only direct annotations, do not try to transfer comments
all_his <- stream_in(file("hypothesis/data/hypothesis.json"), simplifyVector = FALSE) %>% 
  keep(~is.null(.x$references))

h_token = paste("Bearer", Sys.getenv("FV_HIS_TOKEN"))

fv_ii_group <- "7AdKKgAm"
fv_acct <- "acct:frankensteinvariorum@hypothes.is"

# Set permissions so that the new annotation belongs to the FV II group
h_permissions <- list(
  read = list(glue("group:{fv_ii_group}")), 
  admin = list(fv_acct), 
  update = list(fv_acct), 
  delete = list(fv_acct)
)

repost <- function(h, api_url, key) {
  list(
    uri = str_replace(h$uri, "pghfrankenstein.github.io/Pittsburgh_Frankenstein", "frankensteinvariorum.github.io/fv-collation"),
    text = h$text,
    target = h$target,
    group = fv_ii_group,
    permissions = h_permissions
  ) %>% 
    toJSON(auto_unbox = TRUE) %>% 
    POST(api_url, add_headers(Authorization = key), body = ., encode = "json")
}

# Loop through POSTing with a polite rate limit
pb <- progress_bar$new(total = length(all_his), format = ":current [:bar] :percent eta: :eta")
res <- map(all_his, function(h) {
  pb$tick()
  Sys.sleep(1)
  content(repost(h, api_url = h_api, key = h_token))
})
pb$terminate()

# Check for any POST failures
anyNA(map_chr(res, "id"))
