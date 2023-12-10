
   
                                           _____                      _             
                                          / ____|                    (_)            
                                         | (___   ___ _ __ __ _ _ __  _ _ __   __ _ 
                                          \___ \ / __| '__/ _` | '_ \| | '_ \ / _` |
                                          ____) | (__| | | (_| | |_) | | | | | (_| |
                                         |_____/ \___|_|  \__,_| .__/|_|_| |_|\__, |
                                                               | |             __/ |
                                                               |_|            |___/ 



---

## What is it?

**Scraping** is a python program to help in web scraping. 

It uses the library [requests](https://requests.readthedocs.io/en/latest/) to make a get requests and get the web page. 

Then, It uses the library [beautifulsoup4](https://beautiful-soup-4.readthedocs.io/en/latest/) to extract the data inside the html tags.

## Requirements:

install the requests library:

```

python -m pip install requests

```

install the beautifulsoup4:

```

python -m pip install beautifulsoup4

```

## Getting started:

Use the -h to get a list of all valid command-line options:

```

python scraping.py -h

```

output:

```

usage: scraping.py [-h] [-g SITE] [-f FILE] [-o OUTPUT_FILE]

command-line web scrapping program

options:
  -h, --help            show this help message and exit
  -g SITE, --g SITE     site to get the html tag information.
  -f FILE, --file FILE  file to get the html tag information.
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        file to write the tag information.

```

Make a get request to the example.com page:

```

python scraping.py -g www.example.com

```

Get the information in the title tag:

```

[+] Requesting page https://www.example.com
[+] Page returned.

Enter the css selector to extract the tag information: title
[+] Writing the contents to file tag_info_file.txt
[+] Writing completed.

```
View the output file (the default name is tag_info_file.txt):

```

cat tag_info_file.txt

```

output: 

```

Example Domain

```

Getting the information in the html file using class selector:

```

python scraping.py -f example.html

```

```
[+] Getting content from file example.html
[+] File content got.

Enter the css selector to extract the tag information: .books
[+] Writing the contents to file tag_info_file.txt
[+] Writing completed.
```

```

cat tag_info_file.txt

```

Output: 

```
Book one
Book two
Book three

```

To extract the tag information using css selector, the program uses the method **BeautifulSoup.select()**.

See the beautifulsoup4 documentation to learn all the valid values to pass to .select() method:

https://beautiful-soup-4.readthedocs.io/en/latest/#css-selectors





    
