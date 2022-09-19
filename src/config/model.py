from __future__ import annotations

from typing import List, Optional, Union

from pydantic import BaseModel


class _User(BaseModel):
    token: Union[List[str], str]
    id: Optional[int]


class _Bot(BaseModel):
    token: Union[List[str], str]
    id: Optional[int]


class _General(BaseModel):
    user: _User
    group: _Bot
    admins: List[int] = []


class _Regexps(BaseModel):
    links_pattern: str
    hyperlinks_pattern: str
    invite_links_pattern: str
    shortened_links_patterns: str


class _Database(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8090
    user: Optional[str] = None
    password: Optional[str] = None
    database: str = ""
    collection: str = ""
    url: Optional[str] = None


class _Logging(BaseModel):
    log: bool = False
    log_debug: bool = False
    log_errors: bool = False
    log_console: bool = True
    log_path: str = "logs/%Y-%m-%d_%H.log"
    log_errors_path: str = "logs/%Y-%m-%d_%H-error.log"


class _MentionsTrigger(BaseModel):
    user: bool = False
    group: bool = False


class _Triggers(BaseModel):
    mentions: _MentionsTrigger
    invite_links: bool = True
    short_links: bool = True
    invites: bool = True


class _Middlewares(BaseModel):
    no_group_messages: bool = False


class ConfigModel(BaseModel):
    general: _General
    database: _Database
    logging: _Logging
    regexps: _Regexps
    triggers: _Triggers
    middlewares: _Middlewares
