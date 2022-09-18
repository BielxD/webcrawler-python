import requests
import argparse
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(description="search useful information in a website sourge page code\n\nif you want to store the output in a file use the -f argument and specify the path and filename you want to use otherwise the page source code will be printed into the terminal\n\nusage example:\n\ncrawler.py https://google.com\ncrawler.py https://apple.com -r\ncrawler.py https://amazon.com -f /root/Desktop/amazon_page_source.txt\ncrawler.py https://microsoft.com -r -f microsoft_robots.txt\ncrawler.py https://github.com -r -s Allow\ncrawler.py https://facebook.com -r -s disallow -i", formatter_class=RawTextHelpFormatter)
parser.add_argument('url', metavar='url', type=str, help='enter your target url')
parser.add_argument('-r', action='store_true')
parser.add_argument('-f', action='store', default=False)
parser.add_argument('-s', action='store', default=False)
parser.add_argument('-v', action='store', default=5)
parser.add_argument('-i', action='store_true')

args = parser.parse_args()

robots = args.r 
filename = args.f
search = args.s
verbose = args.v
case_insensitive = args.i

if type(verbose) == str:

    if ":" in verbose:

        verbose1 = int(verbose[:verbose.index(":")])
        verbose2 = int(verbose[verbose.index(":") + 1:])

    else:

        verbose1 = int(verbose)
        verbose2 = int(verbose)

else:

    verbose1 = int(verbose)
    verbose2 = int(verbose)


if robots:

    if args.url[-1] == "/":
        url = args.url + "robots.txt"

    else:
        url = args.url + "/robots.txt"

else:

    url = args.url

payload={}
headers = {}
response = requests.request("GET", url, headers=headers, data=payload)

if search:

    if case_insensitive:

        search = search.lower()
        response_case_insensitive = str(response.text.encode('utf8')).lower()
        response_data_formatted = str(response.text.encode('utf8'))

        search_appeareances = response_case_insensitive.count(search)
        last_appeareance = []
        search_data = ""

        for time in range(search_appeareances):

            if last_appeareance:

                response_case_insensitive = response_case_insensitive[last_appeareance[-1]:]
                response_data_formatted = response_data_formatted[last_appeareance[-1]:]

                search_position = response_case_insensitive.index(search)

            else:
            
                search_position = response_case_insensitive.index(search)

            last_appeareance.append(search_position + len(search))
            search_data += response_data_formatted[search_position - len(search) - verbose1:search_position + len(search) + verbose2] + "\n"

    else:

        response_data_formatted = str(response.text.encode('utf8'))
        search_appeareances = response_data_formatted.count(search)
        last_appeareance = []
        search_data = ""

        for time in range(search_appeareances):

            if last_appeareance:

                response_data_formatted = response_data_formatted[last_appeareance[-1]:]

                search_position = response_data_formatted.index(search)

            else:
            
                search_position = response_data_formatted.index(search)

            last_appeareance.append(search_position + len(search))
            search_data += response_data_formatted[search_position - len(search) - verbose1:search_position + len(search) + verbose2] + "\n"

if filename:

    file = open(filename, 'a')

    if search:

        file.write(search_data)

    else:

        file.write(response.text)

    file.close()

else:

    if search:

        print(search_data)

    else:

        print(response.text)