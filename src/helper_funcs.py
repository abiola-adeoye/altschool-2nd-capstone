import tempfile
import os
import json
import shutil

result= {"a": [{"b":2, "c":3}, {"d":4, "e":5}, {"f":6, "g":7}], "h": [{"i":2, "j":3}, {"k":4, "l":5}, {"m":6, "n":7}]}


temp_dir = tempfile.mkdtemp(prefix="unclean_data", suffix="")
for key, value in result.items():
    temp_file_path = os.path.join(temp_dir, f"{key}.json")
    with open(temp_file_path, 'w') as temp_json:
        json.dump(value, temp_json, indent=4)

shutil.move(temp_dir, 'C:/Users/HP/PycharmProjects/altschool-2nd-capstone')