import csv
import json
import os
from typing import List

def write_csv(csv_path: str, row: List) -> None:
    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer_obj = csv.writer(f)
        writer_obj.writerow(row)


def _write_comments(comment_csv_path: str, post_id: str, comments: list) -> None:
    for comment in comments:
        if comment.get('kind') != 't1':
            continue

        comment_data = comment['data']
        write_csv(comment_csv_path, [
            'comment',
            post_id,
            comment_data.get('id'),
            comment_data.get('body'),
        ])

        # fetch this comment's replies (if any)
        # recursively call _write_comments for the replies
        replies = comment_data.get('replies')
        if isinstance(replies, dict):
            reply_children = replies.get('data', {}).get('children', [])
            _write_comments(comment_csv_path, post_id, reply_children)


def scrape_subreddit(posts_json_path: str, comments_dir: str, post_csv_path: str, comment_csv_path: str) -> None:
    '''
    Parses a locally saved subreddit listing JSON (format 'reddit.com/r/{subreddit}/.json')
    plus one comments JSON per post (format 'reddit.com/r/{subreddit}/comments/{post_id}/.json',
    saved as '{comments_dir}/{post_id}.json') into 2 .csv files of
    1. postid -> title, permalink, selftext
    2. postid -> comment_id, body

    Data {}
    Children [{}]
    Data {}
    '''
    write_csv(post_csv_path, ['type', 'post_id', 'title_or_comment_id', 'permalink_or_body', 'selftext'])

    # a. load posts listing
    with open(posts_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    posts = data['data']['children']

    # b. obtain post information
    for post in posts:
        if post.get('kind') != 't3':
            continue
        post_data = post['data']

        post_id = post_data['id']
        title = post_data.get('title')
        permalink = post_data.get('permalink')
        selftext = post_data.get('selftext')

        write_csv(post_csv_path, ['post', post_id, title, permalink, selftext])

        # i. load the comments for this post, if saved
        comment_json_path = os.path.join(comments_dir, f"{post_id}.json")
        if not os.path.isfile(comment_json_path):
            print(f"No comments file found for post {post_id}: {comment_json_path}")
            continue

        with open(comment_json_path, 'r', encoding='utf-8') as f:
            comment_data = json.load(f)

        comments = comment_data[1]['data']['children']

        _write_comments(comment_csv_path, post_id, comments)


if __name__ == '__main__':
    scrape_subreddit('straightedge.json', 'comments', 'straightedge_posts.csv', 'straightedge_comments.csv')