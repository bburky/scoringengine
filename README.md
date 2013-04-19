# Scoring Engine

Minimal proof of concept scoring engine with multiple services

Each service is defined by a python file in the `services/` directory. These scripts are automatically run. APScheduler is used to run the services at a specified frequency.

The `teams.json` file is loaded and is accessible from within the service definitions.

Reports of the tested services are gathered. Currently there is no processing of the collected data.

## Dependencies

*  [APscheduler](https://pypi.python.org/pypi/APScheduler/)
*  [requests](http://docs.python-requests.org/en/latest/) (optional, for http sample service)
*  [paramiko](https://github.com/paramiko/paramiko/) (optional, for ssh sample service)