from moneyball2.etl.db.teams_operations import upsert_team
from moneyball2.etl.requets_api_football.teams_requests import get_teams_by_league


def fetch_teams_by_league(league_id: int, season: int) -> None:
    """
    Fetch teams from the API-Football endpoint for a given league and season,
    and upsert them into the database.

    Args:
        league_id (int): The ID of the league.
        season (int): The season year.
    """
    teams_data = get_teams_by_league(league_id, season)
    if not teams_data or 'response' not in teams_data:
        print("Failed to retrieve teams data.")
        return

    response = teams_data['response']
    if not isinstance(response, list):
        print("Unexpected response format.")
        return

    print(f"Retrieved {len(response)} teams.")
    for team in response:
        team_info = team.get('team')
        if team_info:
            upsert_team(team_info)
        else:
            print("Warning: Missing 'team' key in response item.")
    print("All teams have been upserted successfully.")


if __name__ == "__main__":
    league_id = 140
    season = 2023
    fetch_teams_by_league(league_id, season)
