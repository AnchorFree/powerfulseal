import logging
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from . import AbstractDriver
from ..node import Node, NodeState

def create_host_from_server(server, ip):
    """ Translate Ansible Inventory Instance representation into a Node object.
    """
    return Node(
        id = server.name,
        name = server.name,
        ip = ip,
        groups = server.get_vars()['group_names']
    )

class AnsibleDriver(AbstractDriver):
    """
        Concrete implementation of the Ansible inventory driver.
    """

    def __init__(self, sources=None, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.inventory = InventoryManager(DataLoader(), sources)

    def sync(self):
        """ Downloads a fresh set of nodes form the API.
        """
        self.logger.info("Synchronizing ansible inventory")
        self.inventory.refresh_inventory()
        self.logger.info("Fetched %s remote servers" % len(self.inventory.hosts))

    def get_by_ip(self, ip):
        """ Retreive an instance of Node by its IP.
        """
        host = [ host for host in self.inventory.get_hosts() if host.vars['ansible_host'] == ip]
        if host:
            # Return Node instance for first matched host
            return create_host_from_server(host[0], ip)

    def stop(self, node):
        """ Stop a Node.
        """
        self.logger.info("Stop action for ansible node is not aplicable")

    def start(self, node):
        """ Start a Node.
        """
        self.logger.info("Start action for ansible node is not aplicable")


    def delete(self, node):
        """ Delete a Node permanently.
        """
        self.logger.info("Delete action for ansible node is not aplicable")
