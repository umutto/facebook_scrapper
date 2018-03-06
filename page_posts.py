import json
import datetime
import csv

import utils


def scrape_page_feed(access_token, page_id, since_date, until_date,
                     max_status, out_path):
    """
    Main function to iterate over paginations, statuses and parse them into a csv.
    Main difference between group_posts is the endpoints used.

    page_id: argument can be the name or id of the page.
    """
    out_path = out_path or 'out/pages/'
    with open(f'{out_path}{page_id}_statuses.csv', 'w', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(["status_id", "status_message", "status_author",
                    "link_name", "status_type",
                    "status_link", "status_published", "num_reactions",
                    "num_comments", "num_shares", "num_likes", "num_loves",
                    "num_wows", "num_hahas", "num_sads", "num_angrys",
                    "num_special"])

        num_processed = 0
        start_time = datetime.datetime.now()
        after = ''
        base = "https://graph.facebook.com/v2.9"
        node = f"/{page_id}/posts"
        parameters = f"/?limit={100}&access_token={access_token}"
        date_interval = f"&since={since_date}&until={until_date}"

        print(f"{'='*50}\n{start_time} Scraping facebook page: {page_id}\n")

        # scrapes posts until max_status amount of statuses scraped
        # or there are no more statuses
        while num_processed < max_status:
            after = f"&after={after}" if after else ''
            base_url = base + node + parameters + after + date_interval

            url = utils.get_facebook_page_url(base_url)

            response_url = utils.get_page_response(url)
            if not response_url:
                print("\n{0} Failed! ID: {1} {0}\n{2} Can not get a response..\n"
                      .format('-' * 10, page_id, num_processed))
                return None

            statuses = json.loads(response_url)
            reactions = utils.get_reactions_from_status(base_url)

            for status in statuses['data']:
                # Ensure it is a status with the expected metadata
                if 'reactions' in status:
                    status_data = utils.get_data_from_status(status)
                    reactions_data = reactions.get(status_data[0], None)
                    if reactions_data:
                        # calculate thankful/pride through algebra
                        num_special = status_data[7] - sum(reactions_data)

                        w.writerow(status_data + reactions_data + (num_special, ))

                num_processed += 1
                if num_processed % 100 == 0:
                    print(f"{datetime.datetime.now()} - {num_processed}" +
                          " statuses has been processed.", end='\r')

            # if there is no next page, we're done.
            if 'paging' in statuses:
                after = statuses['paging']['cursors']['after']
            else:
                print()
                break

        print("{0} Done! ID: {1} {0}\n{2} Statuses Processed in {3}\n".format(
            '-' * 10, page_id, num_processed,
            datetime.datetime.now() - start_time))


if __name__ == '__main__':
    config = json.load(open('config.json'))
    app_id = config['app_id']
    app_secret = config['app_secret']
    page_id = "NBC.publicty"

    post_limit_per_page = 500000

    # Input date format should be YYYY-MM-DD
    since_date = "2016-02-24"
    until_date = datetime.datetime.now().strftime('%Y-%m-%d')

    access_token = app_id + "|" + app_secret

    scrape_page_feed(access_token, page_id, since_date, until_date, 150)
