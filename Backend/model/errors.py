class InvalidMimeRequested(Exception):
    def __init__(self, requested_mime: str):
        super().__init__(f"Client requested invalid mime type ({requested_mime})")

class MissingConfigError(Exception):
    def __init__(self, missing_key: str):
        super().__init__(f"Configuration is missing a value for the key '{missing_key}'")

class NameFieldMissing(Exception):
    def __init__(self, origin: str):
        super().__init__(f"No …_name field found in {origin}!")

