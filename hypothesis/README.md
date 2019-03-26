Harvest [hypothes.is](https://hypothes.is) annotations from the Frankenstein Group.

## Requirements

- [curl](https://curl.haxx.se/)
- [jq](https://stedolan.github.io/jq/) ([Tutorial on reshaping JSON with jq](https://programminghistorian.org/en/lessons/json-and-jq))

## Running

While within the `hypothesis/` directory:

1. Get a hypothes.is developer API token and save it in to a file named `.hypothesis_token`

2. Run the script with the command `bash dl_hypothesis.bash`

The script will write to a file called `hypothesis.json` with one JSON object per line (aka [JSONlines](http://jsonlines.org/) formatting)

3. `bash digest_hypothesis.bash` will run a jq command to create a summary table of the annotations

## Sample data

I've saved the first 100 annotations from the Frankenstein group to `sample_hypothesis.json`.

## Current data

`hypothesis.json` is the full output from the Hypothesis API

`hypothesis.csv` is a table extract with:
- h.is ID
- user ID
- date last updated
- text
- tags (`;` delimited)
- start html container
- end html container
- character offset from start container
- character offset from end container
