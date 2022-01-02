   -------------------------
   | OffBoy Automated Tool |
   -------------------------


- This project was defined by 1st line support team, and its approach is 
to have an automated tool to decline all cancelled requests in Siebel and EAI

- In order to know this tool is used , in the following the HLD (HIGH LEVEL DESIGN) will be illustrated

- This project consists of 3 main component :
			= DB data extraction from Siebel and EAI (phase 1) (core) (DONE)
			= useable bot for Sending mails periodically (phase 1) (core) (DONE)
			= Visuallization and reporting every month module (phase 2) (NOT DONE YET)

- This project is being processed as user friendly bot as it can be used for other use cases with different use of ext interfaces and modules
- Reuseable MC's will be mentioned at the end of this documentation

- COMPONENTS :
		
		1- DB Data Extraction :
					Some files are defined to get the data inside extracted as soon as the bot will debug
					it includes : - time (text file)
								  - mail (CSV file)
								  - each_month_rep (CSV file)
					=> time.txt : User can add all possible times he wants to send mail at those paticular added times (it uses the 24-hour clock system)
								 (NOTE : NO. of times that should be added must be more than 1 meaning, User should add 18,12 at least not 18 ONLY).
								 whatever the pattern that the user has added, the module will adapt itself to be sequenced as much as possible.
								 last case, if the user has put times more than 23, it's fine ! however the number will be modulused meaning if he put 24, thus the module will treat it as ZERO (12 AM)
								 (NOTE : the user shoud put each time added in each line)
					=> mail.csv : User can add all possible mails if there are multiple mails as soon as it's valid (still not updated with orange msils)
								  (NOTE : User should enter mail in the right column )
					=> each_month_rep.csv : Actions recorded with number of cancelled orders on Siebel and EAI at their recorded times. (READ ONLY)
					=> initialQuery.txt : this file for the quries that will run for the first time in each of Siebel and EAI DBs
				fn. related for this component : getTime , saveInCSV_MonthReport (3 params) , extractMails
													dataBase_Query_Debug_siebel, dataBase_Query_Debug_eai,
													extract_req_ID
		
		2- Mail Sender (MS) : After Mail and Data extraction OffBoy will send records and details required. This mechanism is done by a GMAIL account called OrangeBot
							  Mail : Orangebot2021@gmail.com
							  Password : (will be sent to one of the team for confidentiallity)
							  Each mail will be sent consists of number orders cancelled mainly . (Using Smtplib)
		3- Visuallization and report : Every day 1 of each month A report with Report of the month previous and a visualization to see rate of growth in orders cancelled on siebel and  EAI each action
			(This is actually the 2nd phase and not the core of the project but IMPORTANT)
- How to Connect to the DataBase :	OffBoy uses mysql connector lib
									first you have to enter the required Host, Username, Password, database name into the blanks on src Code.
									yet, OffBoy doesn't have any files to declare username and password so This should be executed throughout the src Code.
									Extraction data and operation is being done by the dataBase_Query_Debug_eai and dataBase_Query_Debug_siebel methods returning number of orders cancelled in each

Any Issue occured during process or any error caught on the system kindly please contact me on : Alyhassan123456@gmail.com or on 01223522428
 
This tool is Created and authenticated by : Mayar Wael
					    Mohamed Alaa
					    Aly Hassan El Sokkary
Supervised by  : Mahmoud Ibrahim El-bostagy
Department : Information Technology
