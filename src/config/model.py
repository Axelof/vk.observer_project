from __future__ import annotations

from typing import List, Optional, Union

from pydantic import BaseModel


class _Info(BaseModel):
    group_id: int = 0
    user_id: int = 0


class _Bot(BaseModel):
    group_token: Union[List[str], str]
    user_token: Union[List[str], str]
    admins: List[int] = []
    info: _Info = _Info()


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
    log_disable_debug: bool = False
    log_errors: bool = False
    log_console: bool = True
    log_path: str = "logs/%Y-%M-%d_%H-%M-%S.log"
    log_errors_path: str = "logs/%Y-%M-%d_%H-%M-%S-error.log"


class ConfigModel(BaseModel):
    bot: _Bot
    database: _Database
    logging: _Logging
    regexps: _Regexps
