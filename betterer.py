import subprocess
import re

import os


def str_to_int(s: str) -> int:
    return int(s.replace(",", ""))


def get_counts():
    s = """
        This is for testing purposes
        ✅ .eslintrc.betterer.js: ".eslintrc.betterer.js" stayed the same. (13,864
        issues) 😐
        ✅ tsconfig.betterer.json: "tsconfig.betterer.json" stayed the same. (5,771
        issues) 😐
    """
    initial_dir = os.getcwd()
    os.chdir("../glints/api")
    subprocess.run(["git", "pull", "origin"])
    subprocess.run(["yarn"])
    subprocess.run(["rm", "-rf", "dist"])
    subprocess.run(["yarn", "build"])
    out = subprocess.run(["yarn", "betterer:ci"], capture_output=True, encoding="utf8")
    os.chdir(initial_dir)
    s = out.stdout
    es_error_search = re.search(
        '"\.eslintrc\.betterer\.js" stayed the same. \(([\d,]*)', s
    )

    ts_error_search = re.search(
        '"tsconfig\.betterer\.json" stayed the same. \(([\d,]*)', s
    )

    es_error_count = str_to_int(es_error_search.group(1))
    ts_error_count = str_to_int(ts_error_search.group(1))
    return {"es": es_error_count, "ts": ts_error_count}
