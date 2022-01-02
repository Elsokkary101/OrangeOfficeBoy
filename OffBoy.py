import datetime as dt
import smtplib
import os
import mysql.connector
from queue import Queue
import csv
#import sqlite3


path = os.path.dirname(os.path.abspath(__file__))
times = Queue()
# this method is for connecting to the other mail servers
# Using smtp TLS
def sendEmail(message):
    emailUser = 'Orangebot2021@gmail.com'
    emailPass = 'Orange@2021@'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(emailUser, emailPass)
    
    #EMAILing process
    mails = extractMails()
    for mail in mails :
        server.sendmail(emailUser, mail, message)
    server.quit()

def sendEvery (siebel ,eai) :
    total = siebel + eai
    s = 'SRs on Siebel : ' + str(siebel)
    e = 'SRs on EAI : ' + str(eai)
    SUBJECT = 'Daily Report'
    TEXT = 'Dear All, \n\n I hope this mail finds you well and sound \n this is a breif report of SRs of today \n' + s +'\n'+ e + '\n and total is ' + str(total) + " SRs"
    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    sendEmail(message)


def extractMails ():
    word = []
    for strr in open(path+'/mail.csv'):
        word.append(strr)
    return word

# case 1 : if there is only one time
# case 2 : if there're not sorted
# case 3 : if there're not in range 0-23 --> %24

def getTime ():
    time_arr = []
    for strr in open(path + '/time.txt'):
        x = int(strr)
        
        # to be in range 0 - 23
        x = x%24 
        
        time_arr.append(x)
    # if it's not sorted
    time_arr.sort()
    
    #put it in a queue
    for i in time_arr :
        times.put(i)
    
        
''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''

def extractInitialQuery ():
    with open(path + "/InitialQuery.txt","r") as file :
        data = file.read().replace('\n','')
    return data

def saveInCSV_MonthReport(siebel , eai, timeSaved):
    data = [timeSaved,siebel,eai]
    with open(path + "/each_month_rep.csv",'a',newline=('')) as f:
        writer = csv.writer(f)
        writer.writerow(data)
        f.close()

# for siebel
def dataBase_Query_Debug_siebel():
    # please fill in what's missing in database, username and server's password
    sql_connect = mysql.connector.connect(host = 'localhost',
                                          database = '',
                                          user = 'administrator',
                                          passwd = 'administrator')
    if sql_connect.is_connected():
        db_info = sql_connect.get_server_info()
        print('conncected to MySQL Server Version' , db_info)
        cursor = sql_connect.cursor()
        query = extractInitialQuery()
        results = cursor.execute(query).fetchall()
        arr_IDs = extract_req_ID(results)
        ans = IDs_toString(arr_IDs)
        
        #cancel Query
        query = """update ei_orders set ORDER_STATUS = 'Cancelled', FAILURE_REASON = 'manual updated to cancelled'
where order_ref in (""""" + ans + """) and rev_num = 1);""" 
        results = cursor.execute(query) # execute cancellation for one ITEM
        
        query = """update siebel.s_order set status_cd = 'Cancelled' , active_flg ='N' where order_num in (""""" + ans + """) and rev_num = 1;"""
        results = cursor.execute(query)
        return len(arr_IDs)
       
# for EAI
def dataBase_Query_Debug_eai():
    # please fill in what's missing in database, username and server's password
    sql_connect = mysql.connector.connect(host = 'localhost',
                                          database = '',
                                          user = 'administrator',
                                          passwd = 'administrator')
    if sql_connect.is_connected():
        db_info = sql_connect.get_server_info()
        print('conncected to MySQL Server Version' , db_info)
        cursor = sql_connect.cursor()
        query = extractInitialQuery()
        results = cursor.execute(query).fetchall()
        arr_IDs = extract_req_ID(results)
        ans = IDs_toString(arr_IDs)
        
        #cancel Query
        query = """update ei_orders set ORDER_STATUS = 'Cancelled', FAILURE_REASON = 'manual updated to cancelled'
where order_ref in (""""" + ans + """);""" 
        results = cursor.execute(query) # execute cancellation
        return len(arr_IDs)
        

'''      
# for testing   
def dataBase_Query_Debug_eai():
    sql_connect = sqlite3.connect('customer.db')
    cursor = sql_connect.cursor()
    sql_connect.commit()
    query = "select * from customers;"
    results = cursor.execute(query).fetchall()
    arr_IDs = extract_req_ID(results)
    ans = IDs_toString(arr_IDs) # All IDs are readu to be cancelled
    query = """update siebel.s_order set status_cd = 'Cancelled' , active_flg ='N' where order_num in (""""" + ans + """) and rev_num = 1;"""
    print(query)
  '''

      
def extract_req_ID (table):
    counter = 0
    ids = []
    while counter < len(table):
        ids.append(table[counter][0])
        counter = counter + 1
    return ids

def IDs_toString(ids):
    counter = 0
    cancelled = ''
    while counter < len(ids) - 1:
        cancelled = cancelled +"'" +ids[counter] + "',"
        counter += 1
    cancelled = cancelled + "'"+ids[len(ids)-1]+ "'"
    return cancelled

def main():
    getTime()
    time_Caught = times.get()
    while True:
        if times.qsize == 0:
            print("pls enter more than one sending time")
            return
        
        if time_Caught == dt.datetime.now().hour:
            # define variables
            try : 
                orders_in_siebel = dataBase_Query_Debug_siebel()
                orders_in_eai = dataBase_Query_Debug_eai()
                timeSaved = dt.datetime.now()
            

            # Execute CMDs
                sendEvery(orders_in_siebel, orders_in_eai)
                saveInCSV_MonthReport(orders_in_siebel, orders_in_eai, timeSaved)
            
            # update times in Queue
                times.put(time_Caught)  
                time_Caught = times.get()
            except :
                print("Error in System pls report it and troubleshoot")
                return

'''
def main () :
    dataBase_Query_Debug_eai()
'''

if __name__ == "__main__":
    main()

