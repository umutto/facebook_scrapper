import datetime
import json
import argparse
from page_posts import scrape_page_feed
from group_posts import scrape_group_feed

config = json.load(open('config.json'))
app_id = config['app_id']
app_secret = config['app_secret']
access_token = app_id + "|" + app_secret

parser = argparse.ArgumentParser(
    description='Scrapes posts from facebook pages or groups within a time delta.\nRequired arguments are: -i page or group id or -r id file url.')
parser.add_argument('-t', '--type', help='Type of the target site, Default: page',
                    choices=['page', 'group'], default='page')
parser.add_argument(
    '-i', '--id', help='Target ID, string if page, decimal if group')
parser.add_argument('-f', '--file',
                    help="Read from a text file. Where target ID's are seperated by new line.")
parser.add_argument('-s', '--startDate',
                    help='Starting date for the interval where posts will be scraped in, formatted as YYYY-MM-DD. Default: 2016-02-24')
parser.add_argument(
    '-e', '--endDate', help='End date for the interval where posts will be scraped in, formatted as YYYY-MM-DD. Default:  datetime.now')
parser.add_argument(
    '-l', '--limit', help='Max number of statuses to parse per id. Needs to be in intervals of 100 for ease of use. Default: 500,000', type=int, default=500000)
parser.add_argument(
    '-o', '--outPath', help='Output directory to save the resulting csv. Default is out/pages or out/groups.')

args = parser.parse_args()


def parse_posts(parse_type, target_id, date_start, date_end, max_status, out_path):
    """
    Calls appropriate function for scraping facebook pages or groups.
    """
    if parse_type.lower() == 'page':
        scrape_page_feed(access_token, target_id,
                         date_start, date_end,
                         max_status, out_path)
    elif parse_type.lower() == 'group':
        scrape_group_feed(target_id, access_token,
                          date_start, date_end,
                          max_status, out_path)


if __name__ == '__main__':
    """
    This script is used to schedule overnight scraping jobs etc..
    User can feed a text file with group_id's or page_id's seperated by new lines.
    This script will iterate over that given file and output csv's.

    Alternatively, this can be used to scrape a single page from command line.

    For details about arguments use python run.py --help.
    """
    start_date = args.startDate or "2016-02-24"
    end_date = args.endDate or datetime.datetime.now().strftime('%Y-%m-%d')

    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                if line.startswith('#'):
                    continue
                parse_posts(args.type, line.strip(),
                            start_date, end_date, args.limit, args.outPath)
    elif args.id:
        parse_posts(args.type, args.id, start_date,
                    end_date, args.limit, args.outPath)
    else:
        print(
            'Required arguments are not satisfied (target id or file), please see -help')
