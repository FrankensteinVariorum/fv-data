# This script reads out annotations from the first h.is FV group in order to
# migrate them to a centralized account that everyone can easily edit.

library(glue)
library(httr)
library(jsonlite)
library(purrr)
library(progress)

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
    uri = h$uri,
    text = h$text,
    tags = setdiff(h$tags, c("1818", "1831", "Variorum")),
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

# Make a concordance between old and new comment IDs in case we need that for the future.
concordance <- tibble(
  new_id = map_chr(res, "id"),
  old_id = map_chr(all_his, "id")
)

write_csv(concordance, path = "hypothesis/data/concordance-2019-04-13.csv")

# Manual lookup table for comments
comments <- stream_in(file("hypothesis/data/hypothesis.json"), simplifyVector = FALSE) %>% 
  discard(~is.null(.x$references)) %>% 
  map_df(~tibble(regarding = .x$references[[1]], comment = .x$text))

comment_table <- comments %>% 
  left_join(concordance, by = c("regarding" = "old_id")) %>%
  mutate(
    new_annotation = glue("https://hypothes.is/a/{new_id}", .na = NULL),
    old_comment = glue("https://hypothes.is/a/{regarding}", .na = NULL)
  ) %>% 
  select(comment, new_annotation, old_comment)

write_csv(comment_table, path = "hypothesis/data/comment-concordance-2019-04-13.csv")


# RESET ----
# map(res, "id") %>% 
#   map(~DELETE(glue("{h_api}/{.x}"), add_headers(Authorization = h_token))) %>% 
#   map(content)


#content(GET(glue("{h_api}/RvLDFF3xEemrqIv0p6RC3w"), add_headers(Authorization = h_token)))
