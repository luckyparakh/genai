from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class UserInput(BaseModel):
    access_token: str
    project_id: str
    base_url: str


class Commit(BaseModel):
    id: str
    short_id: str
    title: str
    author_name: str
    author_email: str
    created_at: str


class GitLabTagResponse(BaseModel):
    name: str
    message: Optional[str]
    target: str
    commit: Commit


class CommitAuthor(BaseModel):
    name: str
    email: str
    date: datetime


# class Commit(BaseModel):
#     id: str  # Commit SHA
#     short_id: str  # Shortened SHA
#     title: str  # Commit title
#     message: str  # Full commit message
#     author_name: str  # Author's name
#     author_email: str  # Author's email
#     authored_date: datetime  # When the commit was authored
#     committer_name: str  # Committer's name
#     committer_email: str  # Committer's email
#     committed_date: datetime  # When the commit was committed
#     parent_ids: List[str]  # SHA of parent commits
#     web_url: Optional[str]  # URL to the commit in GitLab
#     created_at: datetime


class GitLabCommitsResponse(BaseModel):
    commits: List[Commit]
