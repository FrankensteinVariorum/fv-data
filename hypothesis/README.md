Harvest [hypothes.is](https://hypothes.is) annotations from the Frankenstein Group.

## [View annotation stats to date](https://github.com/PghFrankenstein/fv-data/blob/master/hypothesis/annotations_report.md)


## Running

While within the `hypothesis/` directory:

1. Get a hypothes.is developer API token and save it in to a file named `.hypothesis_token`

2. Run the script with the command `python3 src/dl_hypothesis.py`

The script will write to a file called `data/hypothesis.json` with one JSON object per line (aka [JSONlines](http://jsonlines.org/) formatting)

## Current data

`hypothesis.json` is the full output from the Hypothesis API
