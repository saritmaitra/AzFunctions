#Logging in JSON Format
#If our application generates many logs from different modules, and especially in a microservice architecture, 
# it can be challenging to locate the important logs for your analysis. 
# Therefore, it is best practice to log your messages in JSON format, and send them to a centralized log management system.
# Then we can easily search, visualize, and analyze your log records.
# I would recommend using this Open Source JSON logger: https://github.com/madzak/python-json-logger

pip install python-json-logger

import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()

logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
