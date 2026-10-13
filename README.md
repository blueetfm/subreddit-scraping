# subreddit-scraping

Parses locally saved Reddit JSON listings into CSV files of posts and comments.

## How it works

`main.py` doesn't make any network requests. It reads JSON files you've already
saved to disk and converts them into CSVs:

1. A subreddit listing JSON (e.g. `reddit.com/r/{subreddit}/.json`), saved as
   `straightedge.json` in the repo root.
2. One comments JSON per post (e.g. `reddit.com/r/{subreddit}/comments/{post_id}/.json`),
   saved as `comments/{post_id}.json`.

Running the script produces:

- `straightedge_posts.csv` — one row per post: `type, post_id, title, permalink, selftext`
- `straightedge_comments.csv` — one row per comment (including nested replies):
  `type, post_id, comment_id, body`

If a post's comments file is missing, the script logs a message and skips it
rather than failing.

## Usage

```bash
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt  # if present
python main.py
```

To scrape a different subreddit or file layout, edit the arguments passed to
`scrape_subreddit(posts_json_path, comments_dir, post_csv_path, comment_csv_path)`
at the bottom of [main.py](main.py).

## Reddit JSON "kind" reference

In Reddit API JSON responses, `t1`, `t2`, and `t3` are values for the `kind`
attribute inside a `Thing` object that identify the core data type:

- `t1`: Comment (`t1_...`)
- `t2`: Account / User (`t2_...`)
- `t3`: Link / Submission or Post (`t3_...`)