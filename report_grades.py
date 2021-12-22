import os
import pandas as pd
import re

submissions_path = os.getcwd() + "/submissions/"

all_files = os.listdir(submissions_path)
all_files = list(filter(lambda s: re.match("^submission_[0-9]{9}$", s), all_files))

grades = pd.read_csv("grades_updated.csv")

for submission in all_files:
    
    subid = submission.split('_')[1]
    
    print(f"Submission : {subid}")
    
    subpath = submissions_path + submission
    if not os.path.exists(subpath + "/report.txt"):
        print('skipping')
        continue
    else:
        with open(subpath + "/report.txt", "r") as f:
            report = f.read()
            if report.find("Total Score: ") != -1:
                total_score = float(report[report.find("Total Score: "):].split(": ")[1])
                total_score = min(21, total_score)
                grades.loc[grades["Submission ID"] == int(subid), "2: EasyAI (20.0 pts)"] = total_score

grades.to_csv("grades_updated.csv")

