from typing import Optional


class Version:
    def __init__(self, version: Optional[str] = None, current_git_head=None, release_git_head: Optional[str] = None, repository: Optional[str] = None):
        self.version = version
        self.current_git_head = current_git_head
        self.release_git_head = release_git_head
        self.repository = repository