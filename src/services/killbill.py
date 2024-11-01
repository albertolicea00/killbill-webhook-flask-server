import killbill


class Config:

    def __init__(self, app):

        TENANT = app.config.KB_TENANT

        USERNAME = app.config.KB_USERNAME
        PASSWORD = app.config.KB_PASSWORD
        API_URL = app.config.KB_API_URL
        TIMEOUT = app.config.KB_TIMEOUT

        API_KEY = app.config.KB_API_KEY
        API_SECRET = app.config.KB_API_SECRET
        CREATED_BY = USERNAME

        self.header = killbill.Header(
            api_key=API_KEY,
            api_secret=API_SECRET,
            created_by=CREATED_BY,
        )
        self.api = killbill.KillBillClient(
            username=USERNAME,
            password=PASSWORD,
            api_url=API_URL,
            timeout=TIMEOUT,
        )
