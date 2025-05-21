import os
import sys
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv('./.env')
API_KEY = os.getenv('X_APISPORTS_KEY')
HTTP_OK = int(os.getenv('HTTP_OK', '200'))

if not API_KEY:
    print('Erro: variável de ambiente X_APISPORTS_KEY não definida.')
    sys.exit(1)


def get_teams_by_league(league_id: int, season: int) -> Optional[Dict[str, Any]]:
    """
    Fetch teams from the API-Football endpoint for a given league and season.

    Args:
        league_id (int): The ID of the league.
        season (int): The season year.

    Returns:
        Optional[Dict[str, Any]]: The JSON response as a dictionary if successful, None otherwise.

    Raises:
        requests.RequestException: If there is a connection error.
        Exception: For any other errors.
    """
    url = f'https://v3.football.api-sports.io/teams?league={league_id}&season={season}'
    headers = {'x-rapidapi-host': 'v3.football.api-sports.io', 'x-rapidapi-key': API_KEY}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err} - {response.text}')
    except requests.RequestException as req_err:
        print(f'Request error occurred: {req_err}')
    except Exception as err:
        print(f'An unexpected error occurred: {err}')
    return None


def get_team_statistics(league_id: int, season: int, team_id: int) -> Optional[Dict[str, Any]]:
    """
    Fetch team statistics from the API-Football endpoint for a given league, season, and team.

    Args:
        league_id (int): The ID of the league.
        season (int): The season year.
        team_id (int): The ID of the team.

    Returns:
        Optional[Dict[str, Any]]: The JSON response as a dictionary if successful, None otherwise.
    """
    url = f'https://v3.football.api-sports.io/teams/statistics?league={league_id}&season={season}&team={team_id}'
    headers = {'x-rapidapi-host': 'v3.football.api-sports.io', 'x-rapidapi-key': API_KEY}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err} - {response.text}')
    except requests.RequestException as req_err:
        print(f'Request error occurred: {req_err}')
    except Exception as err:
        print(f'An unexpected error occurred: {err}')
    return None


if __name__ == '__main__':
    # Example usage get_team_statistics
    league_id = 140
    season = 2023
    team_id = 529
    team_statistics = get_team_statistics(league_id, season, team_id)
    if team_statistics:
        print('Team Statistics:')
        print(team_statistics)
    else:
        print('Failed to retrieve team statistics.')
