from dataclasses import dataclass, asdict, field
from typing import Optional, Sequence, List, Dict

import praw


@dataclass
class RedditMetaData:
    post_subreddit: Optional[str] = None
    post_category: Optional[str] = None
    post_title: Optional[str] = None
    post_score: Optional[int] = None
    post_id: Optional[str] = None
    post_url: Optional[str] = None
    post_author: Optional[str] = None

    def serialize(self) -> Dict:
        return asdict(self)


@dataclass
class RedditReader:
    content: str = ""
    meta_data: RedditMetaData = field(default_factory=RedditMetaData)

    def serialize(self) -> Dict:
        return {
            'content': self.content,
            'meta_data': self.meta_data.serialize()
        }


class RedditPostsLoader:
    """Load `Reddit` posts."""

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            user_agent: str,
            search_queries: Sequence[str] = None,
            mode: Optional[str] = "random",
            categories: Sequence[str] = ["new"],
            number_posts: Optional[int] = 10,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.search_queries = search_queries
        self.mode = mode
        self.categories = categories
        self.number_posts = number_posts

    def load(self) -> List[RedditReader]:
        reddit = praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=self.user_agent,
        )

        results: List[RedditReader] = []

        if self.mode == "subreddit":
            for search_query in self.search_queries:
                for category in self.categories:
                    docs = self._subreddit_posts_loader(
                        search_query=search_query, category=category, reddit=reddit
                    )
                    results.extend(docs)
        if self.mode == "random":
            for category in self.categories:
                docs = self._random_posts_loader(
                    category=category, reddit=reddit
                )
                results.extend(docs)

        return results

    def _subreddit_posts_loader(
            self,
            search_query: str,
            category: str,
            reddit: praw.reddit.Reddit) -> List[RedditReader]:
        subreddit = reddit.subreddit(search_query)
        method = getattr(subreddit, category)
        cat_posts = method(limit=self.number_posts)

        readers = []

        for post in cat_posts:
            metadata = RedditMetaData(
                post_subreddit=post.subreddit_name_prefixed,
                post_category=category,
                post_title=post.title,
                post_score=post.score,
                post_id=post.id,
                post_url=post.url,
                post_author=str(post.author)
            )

            reader = RedditReader(
                content=post.selftext,
                meta_data=metadata
            )

            readers.append(reader)

        return readers

    def _random_posts_loader(
            self,
            category: str,
            reddit: praw.reddit.Reddit) -> list[RedditReader]:
        subreddit = reddit.random_subreddit()
        method = getattr(subreddit, category)
        cat_posts = method(limit=self.number_posts)

        readers = []

        """Format reddit posts into a string."""
        for post in cat_posts:
            metadata = RedditMetaData(
                post_subreddit=post.subreddit_name_prefixed,
                post_category=category,
                post_title=post.title,
                post_score=post.score,
                post_id=post.id,
                post_url=post.url,
                post_author=str(post.author)
            )

            reader = RedditReader(
                content=post.selftext,
                meta_data=metadata
            )

            readers.append(reader)

        return readers
