import os
import sys
import praw
import re
from tinydb import TinyDB, Query
import anim
from collections import Counter
import spaw

streamable_username = os.environ.get("streamable_username")
streamable_password = os.environ.get("streamable_password")

reddit_client_id = os.environ.get("reddit_client_id")
reddit_client_secret = os.environ.get("reddit_client_secret")
reddit_refresh_token = os.environ.get("reddit_refresh_token")

_spaw = spaw.SPAW()
_spaw.auth(streamable_username, streamable_password)

db = TinyDB("db.json")

reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    refresh_token=reddit_refresh_token,
    user_agent="/u/objection-bot v0.0",
)


with open('subreddits.txt', 'r') as sublst:
    subreddits = [sub.strip(' \n') for sub in sublst if sub.strip(' \n') != '']

print("starting...")

def get_comment_chain(comment):
    if not isinstance(comment, praw.models.Comment):
        return
    parent_comment = get_comment_chain(comment.parent())
    if parent_comment is not None:
        return [comment, *parent_comment]
    else:
        return [comment]


def get_submission(comment):
    if not isinstance(comment, praw.models.Comment):
        return comment
    else:
        return get_submission(comment.parent())


def init_stream(subreddit_name: str):
    subreddit = reddit.subreddit(subreddit_name)
    return subreddit.stream.comments(pause_after=-1)


User = Query()
comment_streams = [init_stream(subreddit) for subreddit in subreddits]
while True:
    for comment_stream in comment_streams:
        for comment in comment_stream:
            if comment is None:
                break
            if re.search("!objection-*bot", comment.body, re.IGNORECASE):
                if len(db.search(User.id == comment.id)) == 0:
                    try:
                        print(
                            f"doing {comment.id} (https://www.reddit.com{comment.permalink})"
                        )

                        # handle metadata
                        print(f"handling metadata...")
                        db.insert({"id": comment.id})
                        comments = list(reversed(get_comment_chain(comment)))[:-1]
                        authors = [comment.author.name for comment in comments]
                        most_common = [t[0] for t in Counter(authors).most_common()]
                        submission = get_submission(comment)

                        # generate video
                        output_filename = f"{comment.id}.mp4"
                        print(f"generating video {output_filename}...")
                        characters = anim.get_characters(most_common)
                        anim.comments_to_scene(
                            comments, characters, output_filename=output_filename
                        )

                        # upload video
                        print(f"uploading video...")
                        response = _spaw.videoUpload(output_filename)
                        print(response)
                        comment.reply(
                            f"[Here's the video!](https://streamable.com/{response['shortcode']})"
                        )

                        print(f"done {comment.id}")
                    except Exception as e:
                        print(e)
