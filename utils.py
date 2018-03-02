import datetime
import time
import json


try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request


def get_facebook_page_url(base_url, extras=''):
    # Construct the URL string; see http://stackoverflow.com/a/37239851 for
    # Reactions parameters
    fields = ("&fields=message,link,created_time,type,name,id," +
              "comments.limit(0).summary(true),shares,reactions" +
              f".limit(0).summary(true){extras}")

    return base_url + fields


def get_page_response(url, retry_lim=50):
    req = Request(url)

    for i in range(retry_lim):
        try:
            response = urlopen(req)
            if response.getcode() == 200:
                return response.read()
        except Exception as e:
            print(f"{datetime.datetime.now()} - Error for URL {url}\n" +
                  f"{e}\nRetrying{i+1}/{retry_lim}")
            time.sleep(5)


def get_reactions_from_status(base_url):
    reaction_types = ['like', 'love', 'wow', 'haha', 'sad', 'angry']
    reactions_dict = {}

    for reaction_type in reaction_types:
        fields = (f"&fields=reactions.type({reaction_type.upper()})" +
                  ".limit(0).summary(total_count)")
        url = base_url + fields
        response_url = get_page_response(url)
        if not response_url:
            continue
        data = json.loads(response_url)['data']

        data_processed = set()
        for status in data:
            r_id = status['id']
            r_count = status['reactions']['summary']['total_count']
            data_processed.add((r_id, r_count))

        for r_id, r_count in data_processed:
            reactions_dict[r_id] = reactions_dict[r_id] + \
                (r_count,) if r_id in reactions_dict else (r_count, )

    return reactions_dict


def get_data_from_status(status, is_group=False):
    # The status is now a Python dictionary, so for top-level items,
    # we can simply call the key.

    # Additionally, some items may not always exist,
    # so must check for existence first
    status_id = status['id']
    status_type = status['type']

    status_message = status.get('message', '')
    link_name = status.get('name', '')
    status_link = status.get('link', '')

    # Time needs special care since a) it's in UTC and
    # b) it's not easy to use in statistical programs.
    status_published = datetime.datetime.strptime(
        status['created_time'], '%Y-%m-%dT%H:%M:%S+0000')
    status_published = status_published + \
        datetime.timedelta(hours=+9)  # tokyo time
    status_published = status_published.strftime('%Y-%m-%d %H:%M:%S')

    status_author = '' if 'from' not in status else status['from']['name']

    # Nested items require chaining dictionary keys.
    num_reactions = (0 if 'reactions' not in status else
                     status['reactions']['summary']['total_count'])
    num_comments = (0 if 'comments' not in status else
                    status['comments']['summary']['total_count'])
    num_shares = 0 if 'shares' not in status else status['shares']['count']

    return (status_id, status_message, link_name, status_type, status_link,
            status_published, num_reactions, num_comments, num_shares, status_author)
