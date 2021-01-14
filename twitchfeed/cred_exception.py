class CredentialException(Exception):
    """
    Exception raised for wrong authentication credentials (client_id, client_secret)
    """

    def __init__(self, client_id, client_secret):
        message = "Check your authentication credentials: client_id: {}, client_secret: {}".format(client_id, client_secret)
        super().__init__(message)
