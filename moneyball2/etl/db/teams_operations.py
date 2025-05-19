from typing import Any, Dict

from google.cloud.firestore import Client

from moneyball2.etl.db.db import connect_firestore


def upsert_team(team: Dict[str, Any]) -> None:
    """
    Inserts a new team or updates it if it already exists in the Firestore 'teams' collection.

    Args:
        team (Dict[str, Any]): The team entity to insert or update. Must contain an 'id' key.
    """
    db: Client = connect_firestore()
    teams_collection = db.collection('teams')
    team_id = str(team.get('id'))
    if not team_id:
        raise ValueError("Team dictionary must contain a valid 'id' key.")

    try:
        teams_collection.document(team_id).set(team)
    except Exception as e:
        print(f"Failed to upsert team {team.get('name', '<unknown>')} (ID: {team_id}): {e}")
        raise
