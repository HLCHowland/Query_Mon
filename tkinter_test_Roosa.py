import tkinter as tk
import os
import pickle


class GUI:

    def main_menu(self):
        global master
        master = tk.Tk()
        tk.Label(master, text="Main Menu").grid(row=0)

        tk.Button(master, text='Query', command=self.Queries).grid(row=1, column=0, sticky=tk.W, padx=4, pady=4)
        tk.Button(master, text='Monitor', command=self.monitor).grid(row=1, column=2, sticky=tk.W, padx=4, pady=4)
        tk.Button(master, text='Report', command=self.reports).grid(row=1, column=5, sticky=tk.W, padx=4, pady=4)

        tk.Label(master, text="Reports").grid(row=2, column=0, sticky=tk.W)
        tk.Label(master, text="Comparisons").grid(row=2, column=6, sticky=tk.W)

        vertical = tk.Scrollbar(master, orient=tk.VERTICAL)
        vertical.grid(row=2, column=3, rowspan=2, sticky=(tk.N, tk.S))

        horizontal = tk.Scrollbar(master, orient=tk.HORIZONTAL)
        horizontal.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E))

        vertical2 = tk.Scrollbar(master, orient=tk.VERTICAL)
        vertical2.grid(row=2, column=9, rowspan=2, sticky=(tk.N, tk.S))

        horizontal2 = tk.Scrollbar(master, orient=tk.HORIZONTAL)
        horizontal2.grid(row=4, column=4, columnspan=3, sticky=(tk.W, tk.E))

        global reportcount
        reportcount = tk.Listbox(master, yscrollcommand=vertical2.set, xscrollcommand=horizontal2.set,
                                 width=40, height=20)
        reportcount.grid(row=3, column=6, columnspan=3)
        vertical2.config(command=reportcount.yview)
        horizontal2.config(command=reportcount.xview)

        global compare
        compare = tk.Listbox(master, yscrollcommand=vertical.set, xscrollcommand=horizontal.set, width=90, height=20)
        compare.grid(row=3, column=0, columnspan=3)
        vertical.config(command=compare.yview)
        horizontal.config(command=compare.xview)

        tk.mainloop()

    def reports(self):
        self.reportList()
        self.queryScore()

    def reportList(self):
        path = (os.getcwd() + "\Comparisons")
        reporter = os.listdir(path)

        users = []
        report = ''

        for i in range(len(reporter)):
            report = open(path + "\\" + reporter[i], encoding="utf8")

        x = (report.read())
        y = x.splitlines()

        users.append(y)

        bigReport = []
        for i in users:
            for r in i:
                bigReport.append(r)

        finalReport = []
        # included_cols = [0, 3, 4, 5]

        for i in bigReport:
            finalReport.append(i.split(","))
            finalReport.append('\n')

        for row in finalReport:
            compare.insert(tk.END, row)

    def monitor(self):
        monitor_freq = tk.Tk()
        tk.Label(monitor_freq, text='Monitor Freq.').grid(row=0)
        tk.mainloop()


    def queryScore(self):
        path = (os.getcwd() + "\Comparisons")
        reportList = os.listdir(path)

        reports = []

        for i in range(len(reportList)):
            report = open(path + "\\" + reportList[i], encoding="utf8")

            x = (report.read())
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
            if bigListReport[i][1] == "Yes":
                for r in bigFlatScore:
                    if r[0] == bigListReport[i][0]:
                        r[1] += 1

        bigFlatScore.pop(0)
        lists = []

        for row in bigFlatScore:
            lists.append(list(row))
            lists.append('\n')

        for i in lists:
            reportcount.insert(tk.END, i)

    def Queries(self):

        #   Open's up the file and prints out what's in it.
        with open("queries.pickle", "rb") as fp:
            queries = pickle.load(fp)

        #   Button for the selection of the query
        def addItem():
            add = e1.get()
            list.insert('end', add)
            e1.delete(0, 'end')

        def removeItem():
            dele = e2.get()
            for i in dele[::-1]:
                list.delete(i)
            e2.delete(0, 'end')

        root = tk.Tk()
        root.title("Queries")
        root.geometry('480x450')

        #   Add Query
        label = tk.Label(root, text='Add Query', font=('Helvetica', 14, 'bold'))
        label.grid(row=2, column=8)
        e1 = tk.Entry(root)
        e1.grid(row=3, column=8)

        button = tk.Button(root, text='Add', command=addItem)
        button.grid(row=4, column=8)

        #   Delete Query
        label = tk.Label(root, text='Delete Query', font=('Helvetica', 14, 'bold'))
        label.grid(row=6, column=8)
        e2 = tk.Entry(root)
        e2.grid(row=7, column=8)

        button = tk.Button(root, text='Delete', command=removeItem)
        button.grid(row=8, column=8)

        #   Listbox
        label1 = tk.Listbox(root, text='Available Queries', font=('Helvetica', 18, 'bold'))
        label1.grid(row=0, column=0, padx=10, pady=20)

        list = tk.Listbox(root, height=18, width=15, border=0)
        list.grid(row=2, column=0, columnspan=3, rowspan=10, pady=1, padx=5)
        for q in queries:
            list.insert(tk.END, q)

        #   ScrollBar
        scrollbar = tk.Scrollbar(root)
        scrollbar.grid(row=2, column=3, padx=40)


def main():

    run = GUI()
    run.main_menu()


main()
