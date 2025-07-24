
from azure.identity import DefaultAzureCredential
from azure.mgmt.resourcegraph import ResourceGraphClient
from azure.mgmt.resourcegraph.models import QueryRequest 
import pandas as pd
from tabulate import tabulate
from az_arg_queries import arg_queries

class AzureARGQueryHelper:
    
    def __init__(self, subscriptions):
        """
        Initialize the ARG helper with Azure credentials and subscriptions.
        :param subscriptions: List of Azure subscription IDs.
        """
        self.subscriptions = subscriptions
        self.credential = DefaultAzureCredential()
        self.client = ResourceGraphClient(credential=self.credential)

    ## Query is expecting by the dictionaty key not the dictionary value
    def execute_query(self, query_key):

        request = QueryRequest(subscriptions=self.subscriptions, query=arg_queries[query_key])
        response = self.client.resources(request)
        return response.data
    