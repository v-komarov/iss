#coding:utf8

from django.core.management.base import BaseCommand, CommandError
from iss.equipment.models import devices_lldp,devices_ip
import binascii
import networkx as nx


class Command(BaseCommand):
    args = '<graph ...>'
    help = 'saving graph'




    def handle(self, *args, **options):

        G = nx.Graph()


        for ip in devices_ip.objects.all():

            G.add_node(ip.ipaddress)
            nx.set_node_attributes(G, 'location', ip.device_location)
            nx.set_node_attributes(G, 'descr', ip.device_descr)
            nx.set_node_attributes(G, 'name', ip.device_name)

            for row in ip.devices_lldp_set.filter(port_status=True):
                if devices_lldp.objects.exclude(device_ip=ip).filter(port_local_mac=row.port_neighbor_mac,port_status=True).count() != 0:
                    G.add_edge(ip.ipaddress,row.device_ip.ipaddress)
                    break

        #A = nx.nx_agraph.to_agraph(G)
        #A.write('k5_attributes.dot')

        print G.adj

