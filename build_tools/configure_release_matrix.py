import os
import json
from typing import Mapping

def set_github_output(d: Mapping[str, str]):
    """Sets GITHUB_OUTPUT values.
    See https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/passing-information-between-jobs
    """
    print(f"Setting github output:\n{d}")
    step_output_file = os.environ.get("GITHUB_OUTPUT", "")
    if not step_output_file:
        print("Warning: GITHUB_OUTPUT env var not set, can't set github outputs")
        return
    with open(step_output_file, "a") as f:
        f.writelines(f"{k}={v}" + "\n" for k, v in d.items())

def main(args):
    assets = json.loads(args.get("asset_files"))
    release_matrix = []
    for asset in assets:
        asset_name = asset.get("name", "")
        # for now, we can only run tests on mi300 (gfx94X), so hard-coded value here
        if "gfx94X" in asset_name:
            release_matrix.append(asset_name)
            
    set_github_output({
        "release_matrix": json.dumps(release_matrix)
    })

if __name__ == "__main__":
    args = {}
    args["asset_files"] = os.environ.get("ASSET_FILES", "[]")
    main(args)
