"""
Code for copying annotations from the private frankensteinvariorum group over to the public __world__ group so they are viwable by all using hypothes.is
"""

import requests
import json
from tqdm import tqdm
from time import sleep

ann_data = []
with open("data/hypothesis.json", "r") as hj:
    for l in hj:
        ann_data.append(json.loads(l))

his_token = open(".hypothesis_token", "r").read()
his_auth = {"Authorization": f"Bearer {his_token}"}

# for each annotation, re-post to hypothesis as public annotation and then delete the private one
for ann in tqdm(ann_data):
    public_a = ann
    # Remove id, since this will be replaced
    annid = public_a.pop("id", None)
    public_a.pop("created", None)
    public_a.pop("updated", None)
    public_a.pop("links", None)
    public_a.pop("references", None)
    public_a.pop("user_info", None)
    public_a.pop("flagged", None)
    public_a.pop("hidden", None)
    public_a.pop("moderation", None)
    public_a["user"] = "frankensteinvariorum@hypothes.is"
    public_a["group"] = "__world__"
    public_a["permissions"]["read"] = ["group:__world__"]
    public_a["permissions"].pop("admin", None)
    # res = requests.post(
    #     "https://hypothes.is/api/annotations", json=public_a, headers=his_auth
    # )
    # if res.status_code is not 200:
    #     raise Exception("didn't sucessfully transfer {ann}")
    res = requests.delete(
        f"https://hypothes.is/api/annotations/{annid}", headers=his_auth
    )
    sleep(0.5)
