#2019 Henry Howland
#QUERY COMPARISONS
#This program allows the user to enter a list of search queries for Google. The program will find out if there has been
    #a change in the search results for the queries, and then save the differences into their own coherent files. This
    #meant to be used with a SIEM to keep track of changing results on sensitive topics. Output is formatted as CSV with
    #appropriate header.


#Should this script still be used in 2 or so years, it is recommended that a new list of UAs be gathered.



import requests, os, pickle, sys, datetime, time, random, select, re
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



#Allows you to create and modify the list of queries to be monitored.
def queryListInteractor(mainMenuAfter):
    queries = []
#Checking for the query list as seen below is not necessary at this point in the program but just initially informs the user
    #of the lack of a saved queries list (queries.pickle).
    if queryListCheck() == False:
        print("\n    No queries.pickle file found in the CWD.\n    Please create one.\n")
    else:
        with open("queries.pickle", "rb") as fp:
            queries = pickle.load(fp)
#Available commands listed out. > prompt seperated from instructions so instructions not printed after each commanmd.
    print("            QUERIES\n"
          "    Enter query to appended to the 'queries.pickle' file.\n"
          "    'done' when finished.\n"
          "    'list' to look at the numbered query list.\n"
          "    'remove' and the list # of the query to remove it.\n"
          "    'clear' to start over.")
    while True:
#Whole loop in try block incase of unforseen or unaddressed input bug,likeout of bounds remove.
        try:
            prompt = input("> ")
            if prompt == "done":
#Does not just go to main menu when done is typed because there is code at the bottom after the coonditional
    #statement that needs to execute in order to save the code.
                break
            elif prompt == "list":
                if len(queries) == 0:
                    print("\n    Nothing to show.")
                else:
#Used to print the list of queries in a numbered list. Numbered list required for remove method to work properly.
                    for i in range(len(queries)):
                        print("[" + str(i + 1) + "]" + ":", queries[i])
#Command is split up so relevant index can be addressed.
            elif ((prompt.split())[0]) == "remove":
                remove = (int((prompt.split())[1])) - 1
                queries.pop(remove)
                for i in range(len(queries)):
                    print("[" + str(i + 1) + "]" + ":", queries[i])
#Command to clear out list that requires additional yes\no confirmation.
            elif prompt == 'clear':
                confirm = input("\n  Are you sure?\n    yes/no\n> ")
                if confirm == "yes":
                    queries.clear()
            else:
                queries.append(prompt)
        except:
            print("\n    Invalid command!")
#Used to delete the old list and save in its place. There have been issues where the list would not overwrite properly
        # . Not done as .txt file for easier time reading in list object.
        if queryListCheck() == True:
            os.remove("queries.pickle")
        with open("queries.pickle", "wb") as fp:
            pickle.dump(queries, fp)
    queryListRequester(mainMenuAfter, False)
    if mainMenuAfter == 1:
        mainMenu(False)



#Responsible for not only updating the saved search results for comparison after the queries are updated, and the monitor,
    #but also handles the rotating list of query results that the current results are compared against. The slowMode variable is needed,
    #becasue in other functions the frequency of which requests are made is controlled either outside the function, or by
    #the mainMenuAfter variable, but here we cannot use either of those.
def queryListRequester(mainMenuAfter, slowMode):
#First few conditionals check or make the proper files needed for operation.
    searchSetResults = []
    if queryListCheck() == False:
        print("\n    No queries.pickle file found in the CWD.\n    Please create one with the query list editor.\n")
        mainMenu(False)
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
        queryListRequester(mainMenuAfter, False)
    print("\n    Connecting, parsing and pickling...\n")
    for i in range(len(queries)):
#Based on whether this program was called by cron or not, each search will be staggered by between 0 seconds and 7 seconds
    #as to make it more difficult to detect a regular pattern of search, preventing detection and blocking of the bot.
        if slowMode == True:
            time.sleep(random.randint(0,7))
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
                    print("\nConnection failed.\n")
                    if slowMode == True:
                        exit()
                    else:
                        mainMenu(False)
                #print("\n    Connection issues...")
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
        savedResultsRotation[i].append(titles)
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
    if mainMenuAfter == True:
        mainMenu(False)
    return searchSetResults



#Allows you to view the comparison reports.
def reportsInteractor():
#Makes sure comparisons directory is available, if not creating it.
    if comparisonsDirCheck() == False:
        try:
            path = (os.getcwd() + "\Comparisons")
            os.mkdir(path)
        except OSError:
            print("\n    Creation of the 'Comparisons' directory %s failed!" % path)
            mainMenu(False)
        else:
            print("\n    Created the 'Comparisons' directory %s successfully!" % path)
    queries = []
#Checks for 'Comparisons' directory and makes empty one if not there.
    if comparisonsDirCheck() == False:
        try:
            path = (os.getcwd()+"\Comparisons")
            os.mkdir(path)
        except OSError:
            print("\n    Creation of the 'Comparisons' directory %s failed!" % path)
            mainMenu(False)
        else:
            print("\n    Successfully created the 'Comparisons' directory %s successfully!" % path)
    else:
        path = (os.getcwd() + "\Comparisons")
        reportList = os.listdir(path)
    for i in range(len(reportList)):
        for j in range(0, len(reportList) - i - 1):
            if reportList[j] < reportList[j + 1]:
                reportList[j], reportList[j + 1] = reportList[j + 1], reportList[j]
#Available commands listed out. > prompt seperated from instructions so instructions not printed after each command.
    print("            REPORTS\n"
           "    'done' when finished.\n"
           "    'list' to look at the numbered report list.\n"
           "    'read' and the report # to read the file's contents.\n"
           "    'remove' and the report # of the report to remove it.\n"
           "    'clear' empty report list.")
    while True:
# Whole loop in try block incase of unforseen or unaddressed input bug, like out of bounds remove or read.
        try:
            prompt = input("> ")
            if prompt == "done":
                break
            elif prompt == "list":
                if len(reportList) == 0:
                    print("   Nothing to show...")
                else:
# Used to print the report list in a numbered list. Numbered list required for remove method to work properly.
                    for i in range(len(reportList)):
                        print("[" + str(i + 1) + "]" + ":", reportList[i])
# Command is split up so relevant index can be addressed.
            elif ((prompt.split())[0]) == "remove":
                remove = (int((prompt.split())[1])) - 1
                reportList.pop(remove)
                for i in range(len(reportList)):
                    print("[" + str(i + 1) + "]" + ":", reportList[i])
                reportList.clear()
#Command is split up so relevant index can be addressed.
            elif ((prompt.split()))[0] == "read":
                reportNum = (int((prompt.split())[1])) - 1
                report = open(path + "\\" + reportList[reportNum])
                print(report.read())
            elif prompt == 'clear':
                confirm = input("  Are you sure?\n    yes/no\n> ")
                if confirm == "yes":
                    for i in range(len(reportList)):
                        os.remove(path + reportList[i])
#With no reports there is no reason to be in the reports screen.
                    mainMenu(False)
            else:
                print("\n    Invalid command!")
                mainMenu(False)
        except:
            print("\n    Invalid command!")



#The main menu allows access to the list of queries that will be watched, the update which can be used to manually
    #update the query search results for comparison, the monitor which finds the difference between the current query
    #and the saved ones, and the reportsInteractor which is just a shortcut to review reportsInteractor from a particular day.
def mainMenu(initialize):
    if initialize == True:
#Throw away needed because extra input will be made when enter is pressed for initialization, this makes it not an issue.
        input()
        input()
    prompt = input("            MAIN MENU\n"
                   "    'queries' to modify the list of queries to be monitored.\n"
                   "    'reports' to review query search result changes.\n"
                   "    'update' to update the search results of each query.\n"
                   "    'monitor' to start looking for changes.\n"
                   "    'exit' to quit.\n> ")
#Input from prompt will not register correctly sometimes if user does not wait before entering command, most likley due
    #to some way python optimizes itself, waiting 1 second before going on with the prompt fixes this.
    time.sleep(1)
    if prompt == "queries":
        queryListInteractor(True)
    elif prompt == "update":
        queryListRequester(True, False)
    elif prompt == "monitor":
        monitor(True)
    elif prompt == "reports":
        reportsInteractor()
    elif prompt == "exit":
        exit()
        exit()
    else:
        print("\n    Invalid command!")
    mainMenu(False)



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
                print("\n    Connection failed!")
                if mainMenuOnFailure == True:
                    exit()
                else:
                    mainMenu(False)
            print("\n    Connection issues...")
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
        outF.write(line)
        outF.write("\n")
    outF.close()



#Brings all the monitor functions together to compare web pages and save differences based on time interval.
def monitor(mainMenuAfter):
#Below conditionals make sure all files that are needed to run the monitor are available, and will either make them
    #or direct you to make them if they are not.
    if queryListCheck() == False:
        print("\n    No queries.pickle file found in the CWD.\n    Please create one with the query list editor.\n")
        mainMenu(False)
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
            mainMenu(False)
        else:
            print("\n    Created the 'Comparisons' directory %s successfully!" % path)
#Below, if mainMenuAfter == False, then the program is being called via cron. That means that it will be running at a very
        #consistent time. As to prevent bot detection, it waits anywhere between 0 seconds and 2 minutes so query requesting
        #is not consistent.
        if mainMenuAfter == False:
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
    print("\n    Getting results and comparing...")
#Loop to continuously compare search results to everything on the query list.
    for i in range(len(queries) + 1):
        if i > (len(queries)) - 1:
            i =0
#Organizes saved comparisons and resets search results for next run.
            print("")
            monitorComparisonManager(comparisons)
            comparisons = []
#Refreshes query results to current results during next comparison cycle.
            if mainMenuAfter == True:
                queryListRequester(True, False)
            else:
                queryListRequester(False, True)
                time.sleep(5)
                exit()
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



#Checks for additional arguments with program call that allows the program to go straight to monitoring mode. Very useful
    #for checks with crontab.
def initialization():
    try:
#Argument grab
        if __name__ == "__main__":
            x = str(sys.argv[1])
        if x == "mon":
            try:
                monitor(False)
            except IndexError:
                monitor(False)
    except IndexError:
            print("               _________________"
                  "\n              |QUERY COMPARISONS|\n\n"
                  "                  (enter x2)")
#Establishes 10 second time to press enter, if not exits.
    #i, o, e = select.select([sys.stdin], [], [], 30)
            # if (i):
            #     pass
            # else:
            #     exit()
    mainMenu(True)
initialization()
