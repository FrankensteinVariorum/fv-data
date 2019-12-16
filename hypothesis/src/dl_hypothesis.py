import requests
import json
from tqdm import tqdm
from time import sleep

HYPOTHESIS_TOKEN = open(".hypothesis_token", "r").read()
DL_FILE = "data/hypothesis.json"
PAGE_SIZE = 200

HYPOTHESIS_BASE = "https://hypothes.is/api/search?sort=id&user=acct:frankensteinvariorum@hypothes.is&wildcard_uri=https://frankensteinvariorum.github.io/*"

auth_header = {"Authorization": f"Bearer {HYPOTHESIS_TOKEN}"}

total_annotation_count = requests.get(HYPOTHESIS_BASE, headers=auth_header).json()[
    "total"
]

print(f"{total_annotation_count} total annotations to download")

anns = []
for i in tqdm(range(0, total_annotation_count, PAGE_SIZE)):
    res = requests.get(f"{HYPOTHESIS_BASE}&limit=200&offset={i}", headers=auth_header)
    for r in res.json()["rows"]:
        anns.append(r)
    sleep(0.5)


with open(DL_FILE, "w") as outfile:
    for ann in anns:
        json.dump(ann, outfile)
        outfile.write("\n")
