

import os

def queryScore():
    path = (os.getcwd() + "\Comparisons")
    reportList = os.listdir(path)

    reports = []

    for i in range(len(reportList)):
        report = open(path + "\\" + reportList[i])

        x = (report.read())
        y = []
        y = x.splitlines()

        reports.append(y)

    bigReport = []
    for i in reports:
        for r in i:
            bigReport.append(r)

    bigListReport = []

    for i in bigReport:
        bigListReport.append((i.split(",")))

    score = []

    for i in range(len(bigListReport)):
        score.append([bigListReport[i][0]])
        x = 0
        score[i].append(x)

    flatScore = []
    for i in range(len(score)):
        if score[i][0] not in flatScore:
            flatScore.append(score[i][0])

    bigFlatScore = []
    for i in range(len(flatScore)):
        bigFlatScore.append([flatScore[i],0])

    for i in range(len(bigListReport)):
        if bigListReport[i][2] == "Yes":
            for r in bigFlatScore:
                if r[0] == bigListReport[i][0]:
                    r[1] += 1

    bigFlatScore.pop(0)
    return bigFlatScore

print(queryScore())


