import time
import json
import pyodbc
import textwrap
import datetime
import logging
import azure.functions as func

from configparser import ConfigParser


#below function handling json serialization
def default(o):
    """Converts our Dates and Datetime Objects to Strings.
    To get an ISO 8601 date in string format in Python 3, we used the isoformat function."""
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Python HTTP Database trigger function processed a request.')

    # Initialize the Parser.
    config_parser = ConfigParser()

    # Load the Database Credentials.
    config_parser.read('Az-Function-Http/config.ini')
    database_username = config_parser.get('sec-database', 'database_username')
    database_password = config_parser.get('sec-database', 'database_password')

    logging.info('Loaded Database Credentials.')

    # creating "table_name" parameter.
    table_name = req.params.get('table_name', 'DT_ksg_XBRL')

    # Grba the Drivers.
    logging.info(pyodbc.drivers())

    # Define the Driver.
    driver = '{ODBC Driver 17 for SQL Server}'

    # Create the connection String.
    connection_string = textwrap.dedent('''
        Driver={driver};
        Server={my_server_name},1433;
        Database=sec-filings;
        Uid={username};
        Pwd={password};
        Encrypt=yes;
        TrustServerCertificate=no;
        Connection Timeout=30;
    '''.format(
        driver=driver,
        username=database_username,
        password=database_password
    )).replace("'", "")

    # Create a new connection.
    try:
        cnxn: pyodbc.Connection = pyodbc.connect(connection_string)
    except pyodbc.OperationalError:
        time.sleep(2)
        cnxn: pyodbc.Connection = pyodbc.connect(connection_string)

    logging.info(msg='Database Connection Successful.')

    # Create the Cursor Object.
    cursor_object: pyodbc.Cursor = cnxn.cursor()

    # Execute Query.
    upsert_query = textwrap.dedent("""
    SELECT TOP 100 * FROM [dbo].[{table_name}]
    """.format(table_name=table_name))

    # Execute the Query.
    cursor_object.execute(upsert_query)

    # Fetch all Records.
    records = list(cursor_object.fetchall())

    # Clean-up so we can dump them to JSON.
    records = [tuple(record) for record in records]

    logging.info(str(records[1])) # print 1 record for checking
    
    logging.info(msg='Query Successful.') # alternate print

    if records:

        # Return the Response.
        return func.HttpResponse(
            body=json.dumps(obj=records, indent=4, default=default),
            status_code=200
        )
