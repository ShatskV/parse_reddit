from datetime import datetime, timedelta
import json
from praw import Reddit
from dotenv import load_dotenv
import os
from collections import defaultdict
from prawcore.exceptions import PrawcoreException
from reddit_logger import logger
import argparse

def get_sorted_list_from_dict(data, amount=5):
    sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))
    list_of_dicts = [{key: value} for key, value in sorted_data.items()][:amount]
    return list_of_dicts


def parse_args_from_terminal() -> [str, int, int | None , int]:
    parser = argparse.ArgumentParser(description='Set parameters for subreddit parser:',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-n', '--subreddit_name', help="Name of subreddit", type=str, default='gaming')
    parser.add_argument('-a', '--authors_amount', help="Amount of top authors", type=int, default=5)
    parser.add_argument('-l', '--limit', help="Posts limit, 0 for None", type=int, default=10)
    parser.add_argument('-d', '--days', help="Posts for n days", type=int, default=3)

    args = parser.parse_args()
    subreddit_name = args.subreddit_name
    authors_amount = args.authors_amount
    limit = args.limit
    limit = limit if limit else None
    days = args.days

    return subreddit_name, authors_amount, limit, days


def get_top_authors(subreddit_name: str='gaming', authors_amount: int=5, 
                    limit: int| None=10, days_ago: int=3) -> dict[str, int]:
    client_id=os.getenv('CLIENT_ID')
    user_agent=os.getenv('USER_AGENT')
    secret=os.getenv('SECRET')

    reddit = Reddit(client_id=client_id, 
                    client_secret=secret,
                    user_agent=user_agent
                    )
    
    subreddit = reddit.subreddit(subreddit_name)
    n_days_ago = datetime.now() - timedelta(days=days_ago)
    try:
        posts = subreddit.new(limit=limit)
    except PrawcoreException as e:
        logger.error(e)
    top_authors = defaultdict(int)
    top_commentators = defaultdict(int)
   
    for post in posts:
        if post.created_utc >= n_days_ago.timestamp():
            try:
                post.comments.replace_more(limit=None)
            except PrawcoreException as e:
                logger.error(e)
            top_authors[post.author.name] += 1

            for comment in post.comments.list():
                try:
                    top_commentators[comment.author.name] += 1
                except AttributeError as e:
                    continue

    sorted_authors_by_posts = get_sorted_list_from_dict(top_authors, authors_amount)
    sorted_authors_by_comments = get_sorted_list_from_dict(top_commentators, authors_amount)


    return {'top_authors': sorted_authors_by_posts,
            'top_commentators': sorted_authors_by_comments
            }


def main():
    load_dotenv()
    subreddit_name, authors_amount, limit, days = parse_args_from_terminal()
    try:
        top_authors = get_top_authors(subreddit_name, authors_amount, limit, days)
    except PrawcoreException:
        print('Somthing got wrong, see logs!')
    with open('reddit_results.json', 'w') as file:
        json.dump(top_authors, file, indent=3, ensure_ascii=False)


if __name__ == '__main__':
    main()
