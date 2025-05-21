import os

from google.auth.exceptions import DefaultCredentialsError
from google.cloud import firestore


def connect_firestore():
    """
    Connects to Google Firestore using a service account JSON file.

    Returns:
        firestore.Client: Firestore client instance.

    Raises:
        FileNotFoundError: If the credentials file does not exist.
        DefaultCredentialsError: If authentication fails.
        Exception: For any other errors.
    """
    credentials_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), '..', '..', '..', 'moneyball2-751e9-4c8364afe548.json'
        )
    )

    if not os.path.isfile(credentials_path):
        raise FileNotFoundError(f'Credentials file not found: {credentials_path}')

    if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') != credentials_path:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

    try:
        db = firestore.Client()
        return db
    except DefaultCredentialsError as e:
        raise DefaultCredentialsError(f'Authentication failed: {e}') from e
    except Exception as e:
        raise Exception(f'Failed to connect to Firestore: {e}') from e


if __name__ == '__main__':
    try:
        db = connect_firestore()
        collections = list(db.collections())
        print('Available collections:')
        for collection in collections:
            print(collection.id)
    except Exception as e:
        print(f'Error: {e}')
