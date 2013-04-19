from scoringengine.scoringengine import ScoringEngine, ServiceReport
import requests
import requests.exceptions
import os

SERVICE_NAME = 'http'

ScoringEngine.register_service(SERVICE_NAME)
with open(os.path.join(os.path.dirname(__file__), ('http.sample'))) as f:
    sample_response = f.read()


@ScoringEngine.scheduler.interval_schedule(seconds=10)
def http_all():
    ScoringEngine.logger.info('Scoring http')
    for team in ScoringEngine.teams:
        http(team)


def http(team):
    teamName = team['name']
    host = team['services'][SERVICE_NAME]['host']

    try:
        response = requests.get('http://' + host)
        # Verify that the http response matches the sample
        if response.text == sample_response:
            report(teamName, True)
        else:
            report(teamName, False, 'invalid response')
    except requests.exceptions.RequestException:
        report(teamName, False, 'HTTP error')
    except Exception:
        report(teamName, False, 'error')


def report(team, up, status=''):
    ScoringEngine.report(ServiceReport(team=team, service=SERVICE_NAME, up=up, status=status))
