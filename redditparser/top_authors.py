import logging
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta

from praw.models.comment_forest import CommentForest
from prawcore.exceptions import PrawcoreException
from reddit_logger import logger_init

logger_init()
logger = logging.getLogger('main')


@dataclass(frozen=True, slots=True)
class RedditPost:
    author_name: str
    created_utc: float
    comments: CommentForest


@dataclass(frozen=True, slots=True)
class Comment:
    author_name: str


def get_top_by_author(data: list[RedditPost | Comment]):
    top_authors = defaultdict(int)
    for item in data:
        top_authors[item.author_name] += 1
    return top_authors


def get_comments_authors(posts: list[RedditPost]) -> list[Comment]:
    comments = []
    for post in posts:
        try:
            post.comments.replace_more(limit=None)
        except PrawcoreException as e:
            logger.error(e)
        for comment in post.comments.list():
            try:
                comments.append(Comment(author_name=comment.author.name))
            except AttributeError as e:
                continue
    return comments


def get_sorted_list_from_dict(data, amount=5):
    sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))
    list_of_dicts = [{key: value} for key, value in sorted_data.items()][:amount]
    return list_of_dicts


def sort_posts_by_last_days(posts: list[RedditPost], days_ago=3):
    n_days_ago = datetime.now() - timedelta(days=days_ago)
    sorted_posts = []
    for post in posts:
        if post.created_utc >= n_days_ago.timestamp():
            sorted_posts.append(post)
    return posts
