# facebook_scrapper
Web scraper for facebook posts from groups and pages using graph API.
  
---
This is a port of [facebook page post scrapper](https://github.com/minimaxir/facebook-page-post-scraper) from [minimaxir](https://github.com/minimaxir). 
  
I've been using this script for a while and been patching things to fit my use case. It ended up beeing a mutant version of the original, so I've made a careless refactoring recently and decided to put on my github.

I've decided to leave the original comments as is, but added some extra information.
  
All credit belongs to [minimaxir](https://github.com/minimaxir).

---
example use:

Scraping a single page.
```bash
python run.py -i Facebook
```

Feeding a file of group names seperated by new line.
```bash
python run.py -f group_names.txt -t group
```

see `python run.py --help` for more information on arguments:

```bash
python run.py --help
usage: run.py [-h] [-t {page,group}] [-i ID] [-f FILE] [-s STARTDATE]
              [-e ENDDATE] [-l LIMIT] [-o OUTPATH]

Scrapes posts from facebook pages or groups within a time delta. Required
arguments are: -i page or group id or -r id file url.

optional arguments:
  -h, --help            show this help message and exit
  -t {page,group}, --type {page,group}
                        Type of the target site, Default: page
  -i ID, --id ID        Target ID, string if page, decimal if group
  -f FILE, --file FILE  Read from a text file. Where target ID's are seperated
                        by new line.
  -s STARTDATE, --startDate STARTDATE
                        Starting date for the interval where posts will be
                        scraped in, formatted as YYYY-MM-DD. Default:
                        2016-02-24
  -e ENDDATE, --endDate ENDDATE
                        End date for the interval where posts will be scraped
                        in, formatted as YYYY-MM-DD. Default: datetime.now
  -l LIMIT, --limit LIMIT
                        Max number of statuses to parse per id. Needs to be in
                        intervals of 100 for ease of use. Default: 500,000
  -o OUTPATH, --outPath OUTPATH
                        Output directory to save the resulting csv. Default is
                        out/pages or out/groups.
  ```
