from dispatch_backend.DispatchClients import DispatchClients
import json
import typing

class DispatchController:
    def __init__(self):
        self.dispatch_clients = []

    def register_dispatch_client(self, clients: DispatchClients):
        self.dispatch_clients.append(clients)

    def handle_request(self, json_str):
        response_dict = {"status": "ERROR"}
        return response_dict