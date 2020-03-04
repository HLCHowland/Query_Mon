#Henry Howland, Michael Roosa, Janak Malla, Ekaitz Alonso
#Query Monitor
#This program shows you how often the search results for a given list of queries is changing, allowing a user to know
    #when there is an increase of activity on a subject on the internet. This can be used to track current events in a
    #passive way.

#Only non-default packages are requests and bs4
import requests, os, pickle, sys, datetime, time, random, threading, re, tkinter as tk
from bs4 import BeautifulSoup

#Pickling, a method of saving python data structures utilized here, is a very recursive process and would fail without
    #a high recursion limit.
sys.setrecursionlimit(20000)

#The user agent (UA) gives information on who is sending a request for info to a website. We require multiple different UAs
    #so that websites don't see the same requests coming from the same UAs all the time or they will think that the requester
    #is an unwanted automated service taking their infrastructure's resources, which it is.
    #These user agents are current as of June 2019.
userAgents = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Mozilla/5.0 (Linux; U; Android 2.2) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532G Build/MMB29T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.83 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 7.0; SM-G570M Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Mobile/15E148 Safari/604.1',
    'Outlook-iOS/709.2226530.prod.iphone (3.24.1)',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16D57',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A404',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 Mobile/14F89 Safari/602.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0 Mobile/15C153 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0 Mobile/15D60 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0 Mobile/15C202 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_2 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B202 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 9; SM-G965F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 7.0; SM-J730GM Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5',
    'Mozilla/5.0 (iPad; CPU OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; BOIE9;ENUS)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; MS-RTC LM 8; InfoPath.2)',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.28) Gecko/20120306 YFF3 Firefox/3.6.28 ( .NET CLR 3.5.30729; .NET4.0C)',
    'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5',
    'Mozilla/5.0 (iPad; U; CPU OS 4_3_5 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8L1 Safari/6533.18.5',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2; .NET CLR 1.1.4322; InfoPath.1; MS-RTC LM 8)',
    'Opera/9.20 (Windows NT 6.0; U; en)',
    'Mozilla/5.0 (compatible; NetcraftSurveyAgent/1.0/cc-prepass-https; +info@netcraft.com)',
    'Opera/9.01 (Windows NT 5.1; U; en)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.38 Safari/533.4',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.5 Safari/534.55.3',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E; MS-RTC LM 8; InfoPath.1)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; InfoPath.1; .NET4.0C; .NET4.0E; MS-RTC LM 8)']


#Makes sure query list is present, needed to find what monitor.
def queryListCheck():
    path = os.path.isfile(
        os.getcwd() + "\queries.pickle")
    if path:
        return True
    return False



#Checks that previous search page images are available to check the new search pages images against.
def pageImagesCheck():
    path = os.path.isfile(os.getcwd() + "\query-results.pickle")
    if path:
        return True
    return False



#Checks that previous search page images are available to check the new search pages images against. Pages are rotated fifo.
def rotatingPageImagesCheck():
    path = os.path.isfile(os.getcwd() + "\query-results-rotating-list.pickle")
    if path:
        return True
    return False



#Checks for the comparison directory, where the results of the comparisons are stored. No where for splunk to
    #pull comparisons from without it.
def comparisonsDirCheck():
    path = (os.getcwd() + "\Comparisons")
    if os.path.exists(path) == True:
        return True
    return False


def queryListRequester():
#First few conditionals check or make the proper files needed for operation.
    searchSetResults = []
    if queryListCheck() == False:
        pass
    else:
        with open("queries.pickle", "rb") as fp:
            queries = pickle.load(fp)
#If there is no rotating search terms list set up yet, this will make and save the empty list of lists needed to start it.
    #A list of lists is needed so each list can correspond to a query.
    if not rotatingPageImagesCheck():
        x = []
        for i in range(len(queries)):
            x.append([])
        with open("query-results-rotating-list.pickle", "wb") as fp:
            pickle.dump(x, fp)
    with open("query-results-rotating-list.pickle", "rb") as fp:
        savedResultsRotation = pickle.load(fp)
#This is very important, will delete rotating search result images if there is a difference in length between the rotating
    #list and the query length, the only implimented way to tell if the query list has changed.
    if len(savedResultsRotation) != len(queries):
        os.remove("query-results-rotating-list.pickle")
        queryListRequester()
    for i in range(len(queries)):
#Based on whether this program was called by cron or not, each search will be staggered by between 0 seconds and 7 seconds
    #as to make it more difficult to detect a regular pattern of search, preventing detection and blocking of the bot.
#The google search is created with each query being placed inside.
        google_url = "https://www.google.com/search?q={" + queries[i] + "}&num=lnms"
#Try block used in case of connection failure, depending on whether the program is being called by cron or not, it will
    #fail out to the menu or not.
        tryCount = 0
        response = None
        while response is None:
            try:
#The response to the search query from google is taken. The custom user agents are used so the website doesnt realize the
    #itsbeing scraped.
                response = requests.get(google_url, {"User-Agent": userAgents[random.randint(0,(len(userAgents)-1))]})
            except:
                if tryCount == 5:
                    pass
#Beautiful soup gets the html from the response.
        html = BeautifulSoup(response.text, "html.parser")
        result_div = html.find_all('div', attrs={'class': 'ZINbbc'})
        links = []
        titles = []
        descriptions = []
#Parses the html of google search page into lists of the links, titles, and descriptions of the query search results.
        for r in result_div:
#Checks if each element is present, else, raise exception.
            try:
                link = r.find('a', href=True)
                title = r.find('div', attrs={'class': 'vvjwJb'}).get_text()
                description = r.find('div', attrs={'class': 's3v9rd'}).get_text()
#Makes sure everything is present before appending.
                if link != '' and title != '' and description != '':
                    links.append(link['href'])
                    titles.append(title)
                    descriptions.append(description)
#Goes to next loop if one element is not present.
            except:
                continue
        try:
            savedResultsRotation[i].append(titles)
        except:
            continue
        searchResults = [links, titles, descriptions]
        searchSetResults.append(searchResults)
    with open("query-results.pickle", "wb") as fp:
        pickle.dump(searchSetResults, fp)
#This shows the rotating lifo search list's rotation schedule. Here we have the line "if len(savedResultsRotation[0]) == 8:"
    #Each time this function is called a new set of titles from the searches is added to this list. Ideally, when comparing
    #our new search against our old ones, we will be comparing against the search results of the previous 8 searches.
    #It is important to rotate our search results like this, because many search results may go in and out of the search
    #pages remaining a popular topic, we want to know about results that are new, so we compare against lots of old.
    if len(savedResultsRotation[0]) == 8:
        for i in range(len(savedResultsRotation)):
#Deletes oldest list of search results once 8 search results is met.
            savedResultsRotation[i].pop(0)
    with open("query-results-rotating-list.pickle", "wb") as fp:
        pickle.dump(savedResultsRotation, fp)
    return searchSetResults

#Compares the lifo rotating query result list to the current query results for differences, presenting them in comprehensible manner.
def monitorComparer(old, new, query, i):
    if rotatingPageImagesCheck() == False:
        x = []
        with open("query-results-rotating-list.pickle", "wb") as fp:
            pickle.dump(x, fp)
    with open("query-results-rotating-list.pickle", "rb") as fp:
        savedResultsRotation = pickle.load(fp)
#Checks to see if the savedResultRotation variable is populated, and if it should therefore be used.
    if len(savedResultsRotation[0]) == 0:
        comp = old[1]
    else:
        comp = []
#Unloads the saveResultRotation variable so it can be tested against the current results.
        for l in range(len(savedResultsRotation[i])):
            for r in range(len(savedResultsRotation[i][l])):
                comp.append(savedResultsRotation[i][l][r])
    diffs = []
    output = []
#Section makes comparison as well as formats answer.
    for i in range(len(new[1])):
        # link = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', new[0][i])
        # link = link[0].split('/&sa')
        now = datetime.datetime.now()
        dateTime = (now.strftime("%Y-%m-%d %H:%M:%S"))
        if new[1][i] not in comp:
#Reg ex needed to pull link out of what is stored as link. Then commas pulled out of headline and description to produce
    #a .csv file.
            grosslink = new[0][i]
            link = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', grosslink)
            link = link[0].split('&sa')
            headline = new[1][i].replace(',', '')
            description = new[2][i].replace(',','')
            diffs.append(query+","+ dateTime+",Yes,"+headline+","+description+","+link[0])
        output = "\n".join(str(x) for x in diffs)
    if len(output)==0:
        now = datetime.datetime.now()
        dateTime = (now.strftime("%Y-%m-%d %H:%M:%S"))
        output = query + ","+ dateTime+ ",No,No New Headline,No New Description,No New Link"
    return output



#What takes the query list, and gets the results of each search, parses them to be understandable, and sends them off
    #within the monitor method to be compared to the older search results.
def monitorRequester(queries, i, mainMenuOnFailure):
# The google search is created with each query being placed inside.
    google_url = "https://www.google.com/search?q={" + queries[i] + "}&num=lnms"
#Try block used in case of connection failure, depending on whether the program is being called by cron or not, it will
    #fail out to the menu or not.
    tryCount = 0
    response = None
    while response is None:
        try:
#The response to the search query from google is taken. The custom user agents are used so the website doesnt realize the
    #search is coming from a bot.
            response = requests.get(google_url, {"User-Agent": userAgents[random.randint(0,(len(userAgents)-1))]})
        except:
            if tryCount == 5:
                exit()
            tryCount += 1
            pass
#Beautiful soup gets the html from the response.
    html = BeautifulSoup(response.text, "html.parser")
    result_div = html.find_all('div', attrs={'class': 'ZINbbc'})
    links = []
    titles = []
    descriptions = []
#Parses the html of google search page into lists of the links, titles, and descriptions of the query search results.
    for r in result_div:
#Checks if each element is present, else, raise exception.
        try:
            link = r.find('a', href=True)
            title = r.find('div', attrs={'class': 'vvjwJb'}).get_text()
            description = r.find('div', attrs={'class': 's3v9rd'}).get_text()
#Makes sure everything is present before appending.
            if link != '' and title != '' and description != '':
                links.append(link['href'])
                titles.append(title)
                descriptions.append(description)
#Goes to next loop if one element is not present.
        except:
            continue
    searchResults = [links, titles, descriptions]
    return searchResults

#Responsible for saving the results of the comparison as well as organizing them each time to make it easier for whatever
    #is reading them to keep track of and understand them.
def monitorComparisonManager(comparisons):
#Gets list of comparisons currently in 'Comparisons' directory.
    path = (os.getcwd()+"\Comparisons")
    reportList = os.listdir(path)
#Change the end of next line to increase or decrease the amount of files to keep in the rotation.
    if len(reportList) == 30:
#Bubble sort used to sort dates to ensure oldest date is deleted.
        for i in range(len(reportList)):
            for j in range(0, len(reportList) - i - 1):
                if reportList[j] > reportList[j + 1]:
                    reportList[j], reportList[j + 1] = reportList[j + 1], reportList[j]
        delete = reportList[0]
        os.remove(path + delete)
#The name for the files is made using the current date time.
    now = datetime.datetime.now()
    dateTime = (now.strftime("%Y-%m-%d-%H-%M-%S"))
    path = (os.getcwd()+"\Comparisons")
#Query comparison in name below so that each file can be picked up as the same sourcetype even though the file names are
#different with reg-ex. This is done specifically to optimize splunk's sourcetype assignment.
    output = (path + "\comparison-report-"+dateTime+".csv")
    outF = open(output, "w")
#The new report text file is written here. The line directly below is the header for the csv file.
    outF.write("query,dateTime,changeBool,headline,description,link\n")
    for line in comparisons:
        #
        # print(line.count(','))
        # print(line)
        try:
            #If it fails there was an encoding error.
            outF.write(line)
        except:
            continue
        outF.write("\n")
    outF.close()
    # print(comparisons)

#Brings all the monitor functions together to compare web pages and save differences based on time interval.
def monitor():
    mainMenuAfter = False
#Below conditionals make sure all files that are needed to run the monitor are available, and will either make them
    #or direct you to make them if they are not.
    if queryListCheck() == False:
        print("\n    No queries.pickle file found in the CWD.\n    Please create one with the query list editor.\n")
        #mainMenu(False)
    else:
        with open("queries.pickle", "rb") as fp:
            queries = pickle.load(fp)
    if pageImagesCheck() == False:
        print("\n    No query-results.pickle file found in the CWD.\n    Making one now...")
        queryListRequester([])
    else:
        with open("query-results.pickle", "rb") as fp:
            savedResults = pickle.load(fp)
    if comparisonsDirCheck() == False:
        try:
            path = (os.getcwd() + "\Comparisons")
            os.mkdir(path)
        except OSError:
            print("\n    Creation of the 'Comparisons' directory %s failed!" % path)
            #mainMenu(False)
        else:
            print("\n    Created the 'Comparisons' directory %s successfully!" % path)
#Below, if mainMenuAfter == False, then the program is being called via cron. That means that it will be running at a very
        #consistent time. As to prevent bot detection, it waits anywhere between 0 seconds and 2 minutes so query requesting
        #is not consistent.
        #if mainMenuAfter == False:
            time.sleep(random.randint(0, 120))
#The list of queries is taken, and then a list of its indexes, but shuffled is created. This new object if a list of the
    #queries list's indices randomized. This makes bot detection more difficult because a list of the same
    #search queries will not be seen IN ORDER by the server.
    shuffledIndicies = []
    for i in range(len(queries)):
        while True:
            randomIndex = random.randint(0, (len(queries) - 1))
            if randomIndex not in shuffledIndicies:
                shuffledIndicies.append(randomIndex)
                break
#Empty comparisons list populated in loop below.
    comparisons = []
#Loop to continuously compare search results to everything on the query list.
    for i in range(len(queries) + 1):
        if i > (len(queries)) - 1:
            i =0
#Organizes saved comparisons and resets search results for next run.
            monitorComparisonManager(comparisons)
            comparisons = []
#Refreshes query results to current results during next comparison cycle.
            if mainMenuAfter == True:
                queryListRequester()
#Makes each one wait so the searches are not as consistent, to make the bot harder to detect.
        if mainMenuAfter == False:
            time.sleep(random.randint(1,7))
#Conditionals used below to change the behavior of the monitorRequester depending on if cron is calling the program.
        if mainMenuAfter == False:
            currentResults = monitorRequester(queries, shuffledIndicies[i], True)
        else:
            currentResults = monitorRequester(queries, shuffledIndicies[i], False)
#Compares results here.
        comparison = monitorComparer(savedResults,currentResults, queries[shuffledIndicies[i]], shuffledIndicies[i])
        comparisons.append(comparison)
        i += 1

class GUI:

    def main_menu(self):
        global master
        master = tk.Tk()
        master.title("Searching for a Change")
        tk.Label(master, text="Main Menu", font=('Helvetica', 16, 'bold')).grid(row=0, column=0)

        tk.Button(master, text='Query', command=self.Queries).grid(row=1, column=0, sticky=tk.W, padx=4, pady=4)
        tk.Button(master, text='Monitor', command=self.monitor).grid(row=1, column=2, sticky=tk.W, padx=4, pady=4)
        tk.Button(master, text='Report', command=self.reports).grid(row=1, column=6, sticky=tk.W, padx=4, pady=4)

        tk.Label(master, text="Reports", font=('Helvetica', 14, 'bold')).grid(row=2, column=0, sticky=tk.W)
        tk.Label(master, text="Comparisons", font=('Helvetica', 14, 'bold')).grid(row=2, column=6, sticky=tk.W)

        vertical = tk.Scrollbar(master, orient=tk.VERTICAL)
        vertical.grid(row=3, column=3, rowspan=1, sticky=(tk.N, tk.S))

        horizontal = tk.Scrollbar(master, orient=tk.HORIZONTAL)
        horizontal.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E))

        vertical2 = tk.Scrollbar(master, orient=tk.VERTICAL)
        vertical2.grid(row=3, column=9, rowspan=1, sticky=(tk.N, tk.S))

        horizontal2 = tk.Scrollbar(master, orient=tk.HORIZONTAL)
        horizontal2.grid(row=4, column=6, columnspan=3, sticky=(tk.W, tk.E))

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
        compare.delete(0, tk.END)
        path = (os.getcwd() + "\Comparisons")
        reporter = os.listdir(path)

        users = []
        for i in range(len(reporter)):
            report = open(path + "\\" + reporter[i])

            x = (report.read())
            x = x.replace('query,', '').replace('dateTime,', '').replace('changeBool,', '').replace('headline,', '').\
                replace('description,', '').replace('link,', '').replace('link', '')
            x = x.replace('Yes,', '')
            y = x.splitlines()
            users.append(y)

        bigReport = []
        for i in users:
            for r in i:
                bigReport.append(r)

        finalReport = []

        for i in bigReport:
            finalReport.append(i.split(","))
            finalReport.append('\n')

        for i in range(len(finalReport)):
            for x in range(len(finalReport[i])):
                if len(finalReport[i]) > 1:
                    if finalReport[i][2] == 'No':
                        finalReport[i] = ''
            if finalReport[i] == '\n':
                finalReport[i] = ''
            if finalReport[i] == ['']:
                finalReport[i] = ''
        finalReport2 =[]
        for i in finalReport:
            for r in i:
                finalReport2.append(r)
            if i != '':
                finalReport2.append('\n')
        for row in finalReport2:
            compare.insert(tk.END, row)


    def monitor(self):
        monitorThread = threading.Thread(target=monitor)
        monitorThread.start()
        return

    def queryScore(self):
        reportcount.delete(0, tk.END)
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
            bigFlatScore.append([flatScore[i], 0])

        for i in range(len(bigListReport)):
            if bigListReport[i][2] == "Yes":
                for r in bigFlatScore:
                    if r[0] == bigListReport[i][0]:
                        r[1] += 1
        bigFlatScore.pop(0)

        finalFlatScore = []

        for i in bigFlatScore:
            if i[1] != 0:
                finalFlatScore.append(i)
        lists = []

        for row in finalFlatScore:
            lists.append(list(row))
            lists.append('\n')

        lists2 = []

        for i in lists:
            for r in i:
                lists2.append(r)

        for i in range(len(lists2)):
            lists2[0+x:2+x] = [':  '.join(map(str, lists2[0+x:2+x]))]
            x +=2

        lists3 = []
        for i in lists2:
            if i != '':
                lists3.append(i)

        for row in lists3:
            reportcount.insert(tk.END, row)

    def Queries(self):

        #   Open's up the file and prints out what's in it.
        with open("queries.pickle", "rb") as fp:
            queries = pickle.load(fp)

        #   Button for the selection of the query
        def addItem():
            add = e1.get()
            list.insert('end', add)
            queries.append(add)
            with open("queries.pickle", "wb") as fp:
                pickle.dump(queries, fp)
            e1.delete(0, 'end')
            #Updates the rotating search results being compared against
            updateThread = threading.Thread(target=queryListRequester)
            updateThread.start()
        def deleteselectedItem():
            try:
                current_selection = list.curselection()
                list.delete(current_selection)
                selectedQuery = str(queries[current_selection[0]])
                for i in range(len(queries)-1):
                    if selectedQuery == queries[i]:
                        queries.pop(i)
                with open("queries.pickle", "wb") as fp:
                    pickle.dump(queries, fp)
            except:
                pass

        def removeItem():
            dele = e2.get()
            for i in range(len(queries) - 1):
                if dele == queries[i]:
                    queries.pop(i)
                    list.delete(i)
                    with open("queries.pickle", "wb") as fp:
                        pickle.dump(queries, fp)
                    e2.delete(0, 'end')
            e2.delete(0, 'end')

        def clearA():
            list.delete(0, tk.END)
            queries.clear()
            with open("queries.pickle", "wb") as fp:
                pickle.dump(queries, fp)

        root = tk.Tk()
        root.title("Queries")
        root.geometry('340x300')

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

        #   Delete with given input
        button = tk.Button(root, text='Delete', command=removeItem)
        button.grid(row=8, column=8)

        #   Clear All
        button1 = tk.Button(root, text='Clear All', command=clearA)
        button1.grid(row=9, column=8)

        #   Delete Selected
        button1 = tk.Button(root, text='Delete Selected', command=deleteselectedItem)
        button1.grid(row=10, column=8)

        list = tk.Listbox(root, height=18, width=30, border=0)
        list.grid(row=2, column=0, columnspan=3, rowspan=10, pady=1, padx=5)
        for q in queries:
            list.insert(tk.END, q)

        # #   ScrollBar
        # scrollbar = tk.Scrollbar(root)
        # scrollbar.grid(row=2, column=3, padx=40)

def main():
    run = GUI()
    run.main_menu()
main()