from apscheduler.scheduler import Scheduler
import os
import glob
import logging
import imp
import json
import collections

ServiceReport = collections.namedtuple('ServiceReport', ['team', 'service', 'up', 'status'])


class ScoringEngine(object):
    logging.basicConfig()
    logger = logging.getLogger('ScoringEngine')

    scheduler = Scheduler(standalone=True)
    teams = []
    reports = []
    services = []

    def __init__(self, teams, services):
        self.load_teams(teams)
        self.load_services(services)

    def load_teams(self, teams):
        with open(teams) as f:
            ScoringEngine.teams = json.load(f)['teams']

    def load_services(self, services):
        """
        Crazy Python magic to load all the python scripts in the `services` directory as modules
        """

        # TODO: all python extensions, .pyc, etc
        for script in glob.iglob(os.path.join(services, '*.py')):
            scriptpath = os.path.abspath(script)
            path = os.path.dirname(scriptpath)
            basename = os.path.basename(scriptpath)
            name = os.path.splitext(basename)[0]

            # ScoringEngine.logger.info('Loading service ' + name)
            fh, filename, desc = imp.find_module(name, [path])
            module = imp.load_module(name, fh, scriptpath, desc)

            # Possibly could keep list of modules/services
            # This would remove register_service()
            # print module.SERVICE_NAME

    def start(self):
        ScoringEngine.scheduler.start()

    @classmethod
    def register_service(cls, service):
        ScoringEngine.logger.info('Registered service ' + service)
        ScoringEngine.services.append(service)

    @classmethod
    def report(cls, service_report):
        if service_report.up:
            ScoringEngine.logger.info(':'.join([service_report.team, service_report.service, "up"]))
        else:
            ScoringEngine.logger.info(':'.join([service_report.team, service_report.service, "down", service_report.status]))
        ScoringEngine.reports.append(service_report)
