import json
import logging
import os
from dataclasses import dataclass

import typer
from praw import Reddit
from prawcore.exceptions import PrawcoreException
from top_authors import (RedditPost, get_comments_authors,
                         get_sorted_list_from_dict, get_top_by_author,
                         sort_posts_by_last_days)
from typing_extensions import Annotated

logger = logging.getLogger('main')

app = typer.Typer(context_settings={"help_option_names": ["-h"]}, add_completion=False)

@dataclass(frozen=True, slots=True)
class RedditConfig:
    user_agent: str
    client_id: str
    secret: str


def load_from_env() -> RedditConfig:
    client_id = os.getenv('CLIENT_ID')
    user_agent = os.getenv('USER_AGENT')
    secret = os.getenv('SECRET')
    reddit_config = RedditConfig(client_id=client_id,
                                 user_agent=user_agent,
                                 secret=secret
                                 )
    return reddit_config


def get_top_authors(reddit_config: RedditConfig, subreddit_name: str='gaming', authors_amount: int=5, 
                    limit: int| None=10, days_ago: int=3) -> dict[str, int]:
    posts = fetch_posts(reddit_config, subreddit_name, limit)
    sorted_posts = sort_posts_by_last_days(posts, days_ago)
    comments = get_comments_authors(sorted_posts)
    top_authors_posts = get_top_by_author(sorted_posts)
    top_commentators = get_top_by_author(comments)
    sorted_authors_by_posts = get_sorted_list_from_dict(top_authors_posts, authors_amount)
    sorted_authors_by_comments = get_sorted_list_from_dict(top_commentators, authors_amount)
    top_authors = {
        'top_authors': sorted_authors_by_posts,
        'top_commentators': sorted_authors_by_comments
    }
    return top_authors


def fetch_posts(reddit_config: RedditConfig, subreddit_name: str='gaming', limit: int| None=10) -> list[RedditPost]:
    client_id = reddit_config.client_id
    user_agent = reddit_config.user_agent
    secret = reddit_config.secret

    reddit = Reddit(client_id=client_id, 
                    client_secret=secret,
                    user_agent=user_agent
                    )
    
    subreddit = reddit.subreddit(subreddit_name)
    try:
        reddit_posts = subreddit.new(limit=limit)
    except PrawcoreException as e:
        logger.error(e)
        raise
    posts = []
    for post in reddit_posts:
        posts.append(RedditPost(author_name=post.author.name,
                               created_utc=post.created_utc,
                               comments=post.comments))
    return posts


@app.command()
def main(subreddit_name: Annotated[str, typer.Option('-n', help='Name of subreddit')] = 'gaming',
         authors_amount: Annotated[int, typer.Option('-a', help='Amount of top authors')] = 5,
         limit: Annotated[int, typer.Option('-l', help='Posts limit, 0 for None')] = 10,
         days: Annotated[int, typer.Option('-d', help='Posts for n days')] = 3) -> None:
    '''
    Set parameters for subreddit parser:
    '''
    reddit_config = load_from_env()
    limit = limit if limit else None
    try:
        top_authors = get_top_authors(reddit_config, subreddit_name, authors_amount, limit, days)
    except PrawcoreException:
        print('Something got wrong, see logs!')

    with open('reddit_results.json', 'w') as file:
        json.dump(top_authors, file, indent=3, ensure_ascii=False)


if __name__ == '__main__':
    app()
