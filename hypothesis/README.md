Harvest <hypothes.is> annotations from the Frankenstein Group.

## Requirements

- [curl](https://curl.haxx.se/)
- [jq](https://stedolan.github.io/jq/) ([Tutorial on reshaping JSON with jq](https://programminghistorian.org/en/lessons/json-and-jq))

## Running

While within the `hypothesis/` directory:

1. Get a hypothes.is developer API token and save it in to a file named `.hypothesis_token`

2. Run the script with the command `bash dl_hypothesis.bash`

The script will write to a file called `hypothesis.json` with one JSON object per line (aka [JSONlines](http://jsonlines.org/) formatting)

## Sample data

I've saved the first 100 annotations from the Frankenstein group to `sample_hypothesis.json`.
