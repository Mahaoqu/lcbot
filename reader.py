import csv

from data import Problem

all_problems = []

# pid,title,title,url,difficulty,
# topics,frequency,acceptance,comp_count,topic_count,
# companies,accepted,submitted,article_solution,video_solution,
# paid_only

def get_problems_from_file():
    with open('pb.csv') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            all_problems.append(
                Problem(
                    id=row[0],title=row[2],url=row[3],
                    difficulty=row[4], topics=row[5].split(';')
                )
            )
