# The function execution context is exposed via a parameter declared as func.HttpRequest. 
# This instance allows a function to access data route parameters, query string values and methods that allow you to return HTTP responses.
# Once defined, the route parameters are available to the function by calling the route_params method.

# Based on the definition from json file, the __init__.py file that contains the function code might look like the following example:

import logging
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello {name}!")
    else:
        return func.HttpResponse(
            "Please pass a name on the query string or in the request body",
            status_code=400
        )
