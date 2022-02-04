from abc import ABC, abstractmethod
import requests

from swagger_server.models.user import User

class OAuthProvider(ABC):
    @abstractmethod
    def get_session(self) -> requests.Session:
        ...

    @abstractmethod
    def login_provider(self, user: User, session: requests.Session) -> None:
        ...