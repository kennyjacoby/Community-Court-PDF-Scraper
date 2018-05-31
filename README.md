# Community-Court-PDF-Scraper
Scrapes a 1,200-page PDF from the City of Eugene into a structured dataset.

I wrote this program after receiving a 1,200-page PDF from the City of Eugene in response to a public records request for raw data.

The City refused to release the raw data, so I wrote this Python program to scrape the data I needed from it into a structured dataset.

There are several ways to approach this problem and software that might be able to do it for you. I already had a pretty good foundation of Python and BeautifulSoup, so rather than pay for a software or learn a new one with no guaranteed results, I decided to go this route.

The program will only work for this particular PDF, but to anyone else encountering similar problems, it should serve as an idea of one way to approach the problem.

INSTRUCTIONS

1. The first step was converting the PDF to HTML. This took about an hour due to the size of the PDF. 

All I did was run the PDF through the program pdf2txt.py from the command line. I didn't write the program to do this. I downloaded it from here. https://github.com/pdfminer/pdfminer.six

There is no need to do it yourself! I already included the file (output.html) in the repository for your reference. The PDF is also included. 

For use with your own PDFs, the command should look like this: 

pdf2txt.py -o output.html file_name.pdf 

2. The next step was parsing the HTML file. I did this using the BeautifulSoup library. It took several hours to write the program, called arraignments.py

The idea was to scrape only the data I needed. It would have taken way too long to try to get all the data. To accomplish this, I considered unique attributes of each field I needed and its location on the page.

For example, to get the defendant's name, I looked for div tags that were within 80 pixels from the left side of the page, were uppercase, contained a comma and did not contain the string "APPOINTED", which distinguished it from the name of the appointed attorney.

For the docket number, I looked for div tags that were seven characters long and less than 300 pixels from the left side of the page, distinguishing it from the PD Case Number.

For the offense, I looked for spans that were Arial size 8.

For the scheduled status type, I looked for div tags that were between 280 and 300 pixels from the left and were 3 or 5 characters long. I also had to identify 5 of the thousands of entries for which there was a null field. 

For the scheduled status date, I looked for div tags that were between 300 and 350 pixels from the left and had a slash in it.

I explain all this in the comments of the file.

Because the HTML file is one long page as opposed to 1,200 on the PDF, I added all the data points and their pixel-distance from the top of the page into arrays. Then, after collecting all the data points, I sorted each array by the pixel-distance to ensure they were captured in order. This is a crucial step, because the HTML conversion sometimes detects tags out of order.
