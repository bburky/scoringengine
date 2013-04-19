from scoringengine.scoringengine import ScoringEngine, ServiceReport
import paramiko
import os

SERVICE_NAME = 'ssh'

ScoringEngine.register_service(SERVICE_NAME)
with open(os.path.join(os.path.dirname(__file__), ('ssh.sample'))) as f:
    sample_response = f.read()


@ScoringEngine.scheduler.interval_schedule(seconds=10)
def ssh_all():
    ScoringEngine.logger.info('Scoring ssh')
    for team in ScoringEngine.teams:
        ssh(team)


def ssh(team):
    teamName = team['name']
    host = team['services'][SERVICE_NAME]['host']
    port = team['services'][SERVICE_NAME]['port']
    username = team['services'][SERVICE_NAME]['username']
    password = team['services'][SERVICE_NAME]['password']

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=port, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command('ls')
        # Test if the ssh output matches exactly
        # Ideally you would only test if a file is included in the output
        if stdout.read() == sample_response:
            report(teamName, True)
        else:
            report(teamName, False, 'invalid response')
    except (paramiko.AuthenticationException, paramiko.BadAuthenticationType):
        report(teamName, False, 'authentication error')
    except paramiko.SSHException:
        report(teamName, False, 'SSH error')
    except Exception:
        report(teamName, False, 'error')
    finally:
        ssh.close()


def report(team, up, status=''):
    ScoringEngine.report(ServiceReport(team=team, service=SERVICE_NAME, up=up, status=status))
