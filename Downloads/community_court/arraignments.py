import bs4
from bs4 import BeautifulSoup
import urllib2
import time
import operator

def main():
	# start the timer
	start_time = time.time() 
	# create a file to write the data
	fw = open("arraignments.txt", "w") 
	# open the HTML file you converted from PDF
	page = urllib2.urlopen('file:output.html') 
	print("souping...\n")
	# create a BeautifulSoup object to parse (this takes about a minute and a half)
	soup = BeautifulSoup(page.read())
	print("getting data...\n")
	# create empty list for each field you'll be scraping
	defendants = []
	dockets = []
	offenses = []
	scheduled = []
	# create an empty string for the scheduled date field
	sched_date = ""
	# find all the "div" tags in the BeautifulSoup object
	divs = soup.findAll("div")
	# iterate the divs
	for div in divs:
		# create an empty string for the defendant field
		defendant = ""
		# check if the div has the 'style' attribute. 
		if div.has_attr("style"):
			attribute = div["style"]
			# check if the style includes 'left' and 'top' fields
			# you need these to track where each div is located on the page
			# since the HTML is one super long page, the top field indicates the order in which each elements appear.
			# you will sort all the elements by 'top' field later
			if "left:" in attribute:
				left = int(attribute.split("left:")[1].split("px;")[0])
				top = int(attribute.split("top:")[1].split("px;")[0])
				# find all the spans within each div
				spans = div.findAll("span")
				# iterate the spans
				for span in spans:
					# check if the contents of the span has at least one element
				 	if len(span.contents) > 0:
				 		# iterate each element in the span contents
				 		for el in span.contents:
				 			# check if the type of the element is a NavigableString (BeautifulSoup's version of a string)
				 			if type(el) == bs4.element.NavigableString:
				 				# trim the string
				 				string = el.strip()
				 				
				 				# ******** GET THE DEFENDANT NAME ********

				 				# check if the div is less than 80 pixels from the left of the page
				 				if left < 80:
				 					# check if the string is the name of the defendant
				 					# we know it's a defendant if it's uppercase, has a comma (the names are in LAST, FIRST format), is not a name suffix (Jr.), and is not a court-appointed attorney (ECKART, WOSTMANN is a law firm)
				 					if string.isupper() and "," in string and string != ", JR" and "APPOINTED" not in string and "ECKART, WOSTMANN" not in string:
										# append a list containing the top coordinates of the div and the defendant name to the defendants array 
										defendant = string.encode("utf8")
										defendants.append([top, defendant])
										# this next if/then is only needed because five of of the thousands of entries have a null scheduled status field
										# the top coordinates for those five entries are listed below 
										# if the div's top coordinates are in the list...
										if top in [81173, 98102, 373603, 457924, 912642]:
											# append the top coordinates and a null field to the scheduled status array
											scheduled.append([top+1, "NULL|NULL"])
								
								# ******** GET THE DOCKET NUMBER ********

								# if the top coordinates are not less than 80 pixels, check if the div is less than 300 pixels from the left of the page
								# this is important because it's not to be confused with the PD Case Number, which is on the right side of the page
								elif left < 300:
									# check is the string is comprised of all digits
									if string.isdigit():
										# you know its a docket number if it is only seven digits long
										if len(string) == 7:
											# append a list containing the top coordinates of the div and the docket number to the docket array
											docket = string.encode("utf8")
											dockets.append([top, docket])
								
								# ******** GET THE SCHEDULED STATUS ********

								# since I only care about the arraignment date, and not the others, I only scrape the first line of the scheduled status list
								# check if the div is between 280 and 300 pixels from the left side of the page
								if 280 < left < 300:
									# here we check for the scheduled status type (the date comes in the next step)
									# check if the sched_date string is empty, because if it's not then we don't want a second status type
									if sched_date == "":
										# we know the scheduled status type is always either 3 or 5 characters long
										if len(string) in [3, 5]:
											# add the scheduled status type to the sched_date string
											sched_date += "{}|".format(string.encode("utf8"))
								# otherwise, check if the div is between 300 and 350 pixels from the left of the page
								elif 300 < left < 350:	
									# we only want to add the date if the scheduled status type is already entered
									# we know the scheduled status type has been entered if the sched_date string is 4 or 6 characters long (the scheduled status type plus the pipe delimiter)
									if len(sched_date) in [4, 6]:
										# we know it's a date if it has a slash
										if "/" in string:
											# add the date to the sched_date string
											sched_date += string.encode("utf8")
						
						# ******** GET THE OFFENSE ********

						# we know the offenses are the only field in the PDF that have size-8 Arial font
						if span["style"] == "font-family: Arial; font-size:8px":
							# add a list containing the top coordinates and offense to the offenses array
							offense = span.contents[0].encode("utf8").strip()
							offenses.append([top, offense])

				# we only want to append the sched_date string to the list if it is 14 or 16 characters long (the date is always 10 characters, the scheduled status type is either 3 or 5, plus the pipe delimiter)
				if len(sched_date) in [14, 16] or sched_date == "NULL|NULL":
					# add a list containing the top coordinates and the sched_date to the scheduled array
					scheduled.append([top, sched_date])
					sched_date = ""
	# sort all four arrays by the top coordinates from least to greatest
	defendants = sorted(defendants)
	dockets = sorted(dockets)
	offenses = sorted(offenses)
	scheduled = sorted(scheduled)
	# all the arrays are the same length, so iterate through them by range, indexing each one
	for i in range(len(defendants)):
		# create a pipe-delimited string containing the second item in each list of the array
		record = "{}|{}|{}|{}\n".format(defendants[i][1], dockets[i][1], offenses[i][1], scheduled[i][1])
		# write the record to the file
		fw.write(record)
		print(record)
	# print the time elapsed
	print('\n{} minutes, {} seconds'.format(int(round((time.time() - start_time)//60)), int(round((time.time() - start_time)%60))))

if __name__ == "__main__":
    main()