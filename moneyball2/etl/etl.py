from moneyball2.etl.db.teams_operations import upsert_team, upsert_team_statistics
from moneyball2.etl.requets_api_football.teams_requests import (
    get_team_statistics,
    get_teams_by_league,
)

REVERSE_RESPONSE = True


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
        print('Failed to retrieve teams data.')
        return
    response = teams_data['response']

    if not isinstance(response, list):
        print('Unexpected response format.')
        return
    print(f'Retrieved {len(response)} teams.')

    for team in response:
        team_info = team.get('team')
        if team_info:
            upsert_team(team_info)
        else:
            print("Warning: Missing 'team' key in response item.")
    print('All teams have been upserted successfully.')


def fetch_teams_statistics(league_id: int, season: int) -> None:
    """
    Fetch teams statistics from the API-Football endpoint for a given league and season,
    and upsert them into the database.

    Args:
        league_id (int): The ID of the league.
        season (int): The season year.
    """
    teams_data = get_teams_by_league(league_id, season)
    if not teams_data or 'response' not in teams_data:
        print('Failed to retrieve teams data.')
        return
    response = teams_data['response']

    if not isinstance(response, list):
        print('Unexpected response format.')
        return
    print(f'Retrieved {len(response)} teams.')

    if REVERSE_RESPONSE:
        response.reverse()

    for team in response:
        team_info = team.get('team')
        if not team_info:
            print("Warning: Missing 'team' key in response item.")
            continue

        team_id = team_info.get('id')
        if not team_id:
            print("Warning: Missing 'id' key in team info.")
            continue

        team_statistics = get_team_statistics(league_id, season, team_id)
        if not team_statistics or 'response' not in team_statistics:
            print(f'Failed to retrieve statistics for team ID {team_id}.')
            continue

        stats_response = team_statistics['response']
        if not isinstance(stats_response, (list, dict)):
            print(f'Unexpected statistics response format for team ID {team_id}.')
            continue

        if isinstance(stats_response, list):
            if not stats_response:
                print(f'No statistics data for team ID {team_id}.')
                continue
            stats_response = stats_response[0]

        if not isinstance(stats_response, dict):
            print(f'Unexpected statistics response format for team ID {team_id}.')
            continue

        team_stats_team = stats_response.get('team', {})
        team_stats_goals_for = stats_response.get('goals', {}).get('for', {}).get('total', {})
        team_stats_goals_against = (
            stats_response.get('goals', {}).get('against', {}).get('total', {})
        )
        team_stats_fixtures = stats_response.get('fixtures', {})

        team_statistics_info = {
            'id': int(f'{team_id}{season}{league_id}'),
            'team': team_stats_team.get('id'),
            'season': season,
            'league_id': league_id,
            'team_name': team_stats_team.get('name'),
            'goals_home': team_stats_goals_for.get('home'),
            'goals_away': team_stats_goals_for.get('away'),
            'goals_total': team_stats_goals_for.get('total'),
            'goals_against_home': team_stats_goals_against.get('home'),
            'goals_against_away': team_stats_goals_against.get('away'),
            'goals_against_total': team_stats_goals_against.get('total'),
            'wins_home': team_stats_fixtures.get('wins', {}).get('home'),
            'wins_away': team_stats_fixtures.get('wins', {}).get('away'),
            'wins_total': team_stats_fixtures.get('wins', {}).get('total'),
            'draws_home': team_stats_fixtures.get('draws', {}).get('home'),
            'draws_away': team_stats_fixtures.get('draws', {}).get('away'),
            'draws_total': team_stats_fixtures.get('draws', {}).get('total'),
            'loses_home': team_stats_fixtures.get('loses', {}).get('home'),
            'loses_away': team_stats_fixtures.get('loses', {}).get('away'),
            'loses_total': team_stats_fixtures.get('loses', {}).get('total'),
        }
        print(f'Upserting statistics for team ID {team_id}: {team_statistics_info}')
        upsert_team_statistics(team_statistics_info)
    print('All team statistics have been upserted successfully.')


if __name__ == '__main__':
    league_id = 140
    season = 2022
    fetch_teams_statistics(league_id, season)
