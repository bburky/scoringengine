#!/usr/bin/env python
import logging
from scoringengine.scoringengine import ScoringEngine

print('Starting scoring engine')

# Output all debugging info
ScoringEngine.logger.setLevel(logging.INFO)

# Setup scoring engine
scoring_engine = ScoringEngine(teams='teams.json', services='services')

print('Press Ctrl+C to exit')
try:
    scoring_engine.start()
except (KeyboardInterrupt, SystemExit):
    pass
