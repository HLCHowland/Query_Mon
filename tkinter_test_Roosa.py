import tkinter as tk
from tkinter.filedialog import askopenfilename
import csv

class GUI:

    def main_menu(self):
        global master
        master = tk.Tk()
        tk.Label(master, text="Main Menu").grid(row=0)

        tk.Button(master, text='Query', command=self.query_list).grid(row=1, column=0, sticky=tk.W, padx=4, pady=4)
        tk.Button(master, text='Monitor', command=self.monitor).grid(row=1, column=3, sticky=tk.W, padx=4, pady=4)
        tk.Button(master, text='Comparisons', command=self.comparisons).grid(row=1, column=6, sticky=tk.W, padx=4, pady=4)

        tk.Label(master, text="Reports").grid(row=2, column=0, sticky=tk.W)
        tk.Label(master, text="Comparisons").grid(row=2, column=4, sticky=tk.W)

        tk.Listbox(master, width=30, height=20).grid(row=3, column=0, columnspan=3)

        global compare
        compare = tk.Listbox(master, width=90, height=20)
        compare.grid(row=3, column=4, columnspan=3)
        tk.mainloop()

    def comparisons(self):
        csv_file_path = askopenfilename()
        print(csv_file_path)
        with open(csv_file_path, 'r', encoding='ascii') as f:
            users = []
            reader = csv.reader(f)
            for row in reader:
                users.append(row)
        for i in users:
            compare.insert(tk.END, i)

    def monitor(self):
        monitor_freq = tk.Tk()
        tk.Label(monitor_freq, text='Monitor Freq.').grid(row=0)
        tk.mainloop()

    def show_entry_fields(self):
        print((e1.get()))

    def query_list(self):
        query = tk.Tk()
        tk.Label(query, text="Add Query").grid(row=0)

        global e1
        e1 = tk.Entry(query)

        e1.grid(row=1, column=0)

        tk.Button(query, text='Enter', command=self.show_entry_fields).grid(row=2, column=0, sticky=tk.W, pady=4)

        tk.mainloop()


def main():
    run = GUI()
    run.main_menu()


main()














































