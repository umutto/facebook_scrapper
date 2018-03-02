import json
import datetime
import csv

import utils


def scrape_group_feed(access_token, group_id, since_date, until_date,
                      max_status, out_path):
    """
    Main function to iterate over paginations, statuses and parse them into a csv.
    Main difference between page_posts is the endpoints used.
    """
    out_path = out_path or 'out/groups/'
    with open(f'{out_path}{group_id}_statuses.csv', 'w', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(["status_id", "status_message", "status_author", "link_name",
                    "status_type", "status_link", "status_published",
                    "num_reactions", "num_comments", "num_shares", "num_likes",
                    "num_loves", "num_wows", "num_hahas", "num_sads", "num_angrys",
                    "num_special"])

        num_processed = 0
        start_time = datetime.datetime.now()
        paging = ''
        base = "https://graph.facebook.com/v2.11"
        node = f"/{group_id}/feed"
        parameters = f"/?limit={100}&access_token={access_token}"
        date_interval = f"&since={since_date}&until={until_date}"

        next_page = None
        paging_list = []
        base_url = ''

        print(f"{'='*50}\n{start_time} Scraping facebook group: {group_id}\n")

        # scrapes posts until max_status amount of statuses scraped
        # or there are no more statuses
        while num_processed <= max_status:
            base_url = (base + node + parameters + date_interval + paging
                        if base_url == '' else next_page)

            url = utils.get_facebook_page_url(base_url, ',from')
            statuses = json.loads(utils.get_page_response(url))
            reactions = utils.get_reactions_from_status(base_url)

            for status in statuses['data']:
                # Ensure it is a status with the expected metadata
                if 'reactions' in status:
                    status_data = utils.get_data_from_status(status, True)
                    reactions_data = reactions[status_data[0]]

                    # calculate thankful/pride through algebra
                    num_special = status_data[6] - sum(reactions_data)

                    w.writerow(status_data + reactions_data + (num_special, ))

                # output progress occasionally to make sure code is not
                # stalling
                num_processed += 1
                if num_processed % 100 == 0:
                    print(f"{datetime.datetime.now()} - {num_processed}" +
                          " statuses has been processed.", end='\r')

            if 'paging' in statuses:
                next_page = statuses['paging'].get('next', None)

            # next_page is acquired if response has a page
            # and it is never seen before (not in paging_list)
            # if there is no next page fitting the requirement, we're done.
            if next_page and next_page not in paging_list:
                paging_list.append(next_page)
            else:
                print()
                break

        print("{0} Done! ID: {1} {0}\n{2} Statuses Processed in {3}\n".format(
            '-' * 10, group_id, num_processed,
            datetime.datetime.now() - start_time))


if __name__ == '__main__':
    config = json.load(open('config.json'))
    app_id = config['app_id']
    app_secret = config['app_secret']
    group_id = "141351322657657"

    post_limit_per_group = 500000

    # Input date format should be YYYY-MM-DD
    since_date = "2016-02-24"
    until_date = datetime.datetime.now().strftime('%Y-%m-%d')

    access_token = app_id + "|" + app_secret

    scrape_group_feed(access_token, group_id, since_date, until_date, 150)
