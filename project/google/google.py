import requests
from loguru import logger
from oauthlib.oauth2 import WebApplicationClient


class Google:
    def __init__(
        self,
        google_client_id=None,
        google_client_secret=None,
        google_discovery_url=None,
    ):

        if (
            google_client_id is None
            or google_client_secret is None
            or google_discovery_url is None
        ):
            logger.info(
                "You need to set google_client_id, google_client_secret and google_discovery_url later"
            )
            self.GOOGLE_CLIENT_ID = None
            self.GOOGLE_CLIENT_SECRET = None
            self.GOOGLE_DISCOVERY_URL = None
            self.client = None
            return

        self.GOOGLE_CLIENT_ID = google_client_id
        self.GOOGLE_CLIENT_SECRET = google_client_secret
        self.GOOGLE_DISCOVERY_URL = google_discovery_url

        self.client = WebApplicationClient(self.GOOGLE_CLIENT_ID)

    def init_google(self, google_client_id, google_client_secret, google_discovery_url):

        if (
            google_client_id is None
            or google_client_secret is None
            or google_discovery_url is None
        ):
            logger.warning(
                "You need to set google_client_id, google_client_secret and google_discovery_url if you want to use google login !"
            )
            return

        if (
            self.GOOGLE_CLIENT_ID is not None
            or self.GOOGLE_CLIENT_SECRET is not None
            or self.GOOGLE_DISCOVERY_URL is not None
        ):
            logger.warning(
                "You have already set google_client_id, google_client_secret and google_discovery_url, all of them will be replaced"
            )

        self.GOOGLE_CLIENT_ID = google_client_id
        self.GOOGLE_CLIENT_SECRET = google_client_secret
        self.GOOGLE_DISCOVERY_URL = google_discovery_url

        self.client = WebApplicationClient(self.GOOGLE_CLIENT_ID)

    def get_google_provider_cfg(self):
        # logger.debug(f"GOOGLE_DISCOVERY_URL: {self.GOOGLE_DISCOVERY_URL}")
        # logger.debug(f"GOOGLE_CLIENT_SECRET: {self.GOOGLE_CLIENT_SECRET}")
        # logger.debug(f"GOOGLE_CLIENT_ID: {self.GOOGLE_CLIENT_ID}")

        return requests.get(self.GOOGLE_DISCOVERY_URL).json()
