# There are 5 different log levels indicating the serverity of events. 
# By default, the system logs only events with level WARNING and above.
import logging
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')

# Configuration
# With basicConfig(**kwargs) we can customize the root logger. 
# The most common parameters are the level, the format, and the filename. 
# https://docs.python.org/3/library/logging.html#logging.basicConfig. 
# https://docs.python.org/3/library/logging.html#logrecord-attributes for possible formats and 
# https://docs.python.org/3/library/time.html#time.strftime how to set the time string. 
# Note that this function should only be called once, and typically first thing after importing the module. 
# It has no effect if the root logger already has handlers configured. 
# For example calling logging.info(...) before the basicConfig will already set a handler.

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
# Now also debug messages will get logged with a different format.
logging.debug('Debug message')

# This would log to a file instead of the console.
# logging.basicConfig(level=logging.DEBUG, filename='app.log')

# Logging in modules and logger hierarchy
# Best practice in our application with multiple modules is to create an internal logger using the __name__ global variable. 
# This will create a logger with the name of our module and ensures no name collisions. 
# The logging module creates a hierarchy of loggers, starting with the root logger, and adding the new logger to this hierarchy. 
# If we then import our module in another module, log messages can be associated with the correct module through the logger name. 
# Note that changing the basicConfig of the root logger will also affect the log events of the other (lower) loggers in the hierarchy.

# helper.py
# -------------------------------------
import logging
logger = logging.getLogger(__name__)
logger.info('HELLO')

# main.py
# -------------------------------------
import logging
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
import helper

# --> Output when running main.py
# helper - INFO - HELLO

# Propagation
# By default, all created loggers will pass the log events to the handlers of higher loggers, in addition to any handlers attached to the created logger. 
# We can deactivate this by setting propagate = False. 

# helper.py
# -------------------------------------
import logging
logger = logging.getLogger(__name__)
logger.propagate = False
logger.info('HELLO')

# main.py
# -------------------------------------
import logging
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
import helper

# --> No output when running main.py since the helper module logger does not propagate its messages to the root logger

#LogHandlers
# Handler objects are responsible for dispatching the appropriate log messages to the handler's specific destination. 
# For example we can use different handlers to send log messaged to the standard output stream, to files, via HTTP, or via Email. 
# Typically we configure each handler with a level (setLevel()), a formatter (setFormatter()), and optionally a filter (addFilter()). 
# https://docs.python.org/3/howto/logging.html#useful-handlers for possible built-in handlers.
# We can also implement our own handlers by deriving from these classes.

import logging

logger = logging.getLogger(__name__)

# Create handlers
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler('file.log')

# Configure level and formatter and add it to handlers
stream_handler.setLevel(logging.WARNING) # warning and above is logged to the stream
file_handler.setLevel(logging.ERROR) # error and above is logged to a file

stream_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(stream_format)
file_handler.setFormatter(file_format)

# Add handlers to the logger
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

logger.warning('This is a warning') # logged to the stream
logger.error('This is an error') # logged to the stream AND the file!

# Example of a filter
class InfoFilter(logging.Filter):
    
    # overwrite this method. Only log records for which this
    # function evaluates to True will pass the filter.
    def filter(self, record):
        return record.levelno == logging.INFO

# Now only INFO level messages will be logged
stream_handler.addFilter(InfoFilter())
logger.addHandler(stream_handler)


# Then use the config file in the code
import logging
import logging.config

logging.config.fileConfig('logging.conf')

# create logger with the name from the config file. 
# This logger now has StreamHandler with DEBUG Level and the specified format
logger = logging.getLogger('simpleExample')

logger.debug('debug message')
logger.info('info message')

# Capture Stack traces
# Logging the traceback in our exception logs can be very helpful for troubleshooting issues. 
# We can capture the traceback in logging.error() by setting the exc_info parameter to True.
import logging

try:
    a = [1, 2, 3]
    value = a[3]
except IndexError as e:
    logging.error(e)
    logging.error(e, exc_info=True)
    
# If you don't capture the correct Exception, you can also use the traceback.format_exc() method to log the exception.
import logging
import traceback

try:
    a = [1, 2, 3]
    value = a[3]
except:
    logging.error("uncaught exception: %s", traceback.format_exc())
    
# Rotating FileHandler
# When we have a large application that logs many events to a file, and we only need to keep track of the most recent events, 
# then use a RotatingFileHandler that keeps the files small. 
# When the log reaches a certain number of bytes, it gets "rolled over". We can also keep multiple backup log files before overwriting them.
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# roll over after 2KB, and keep backup logs app.log.1, app.log.2 , etc.
handler = RotatingFileHandler('app.log', maxBytes=2000, backupCount=5)
logger.addHandler(handler)

for _ in range(10000):
    logger.info('Hello, world!')
    
#TimedRotatingFileHandler
#If our application will be running for a long time, you can use a TimedRotatingFileHandler. 
#This will create a rotating log based on how much time has passed. Possible time conditions for the when parameter are:

#second (s)
#minute (m)
#hour (h)
#day (d)
#w0-w6 (weekday, 0=Monday)
#midnight

import logging
import time
from logging.handlers import TimedRotatingFileHandler
 
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# This will create a new log file every minute, and 5 backup files with a timestamp before overwriting old logs.
handler = TimedRotatingFileHandler('timed_test.log', when='m', interval=1, backupCount=5)
logger.addHandler(handler)
 
for i in range(6):
    logger.info('Hello, world!')
    time.sleep(50)
    
