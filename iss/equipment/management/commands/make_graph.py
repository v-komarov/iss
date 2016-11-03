#coding:utf8

from django.core.management.base import BaseCommand, CommandError
from iss.equipment.models import devices_lldp,devices_ip
import networkx as nx



class Command(BaseCommand):
    args = '<graph ...>'
    help = 'saving graph'




    def handle(self, *args, **options):

        G = nx.Graph()
        #G = nx.complete_graph()

        for ip in devices_ip.objects.all():

            clients = devices_lldp.objects.filter(device_ip=ip,port_neighbor_mac=None,port_status=True).count()

            G.add_node(ip.ipaddress,name=ip.device_name,location=ip.device_location,descr=ip.device_descr,clients=clients,label="\N\nlocalion:%s\ndescr:%s\nname:%s\nclients:%s" % (ip.device_location,ip.device_descr,ip.device_name,clients))
            #nx.set_node_attributes(G, 'location', ip.device_location)
            #nx.set_node_attributes(G, 'descr', ip.device_descr)
            #nx.set_node_attributes(G, 'name', ip.device_name)
            #nx.set_node_attributes(G, 'clients', clients)


            for local in devices_lldp.objects.exclude(port_neighbor_mac=None).filter(device_ip=ip,port_status=True):
                search = devices_lldp.objects.exclude(device_ip=ip).filter(port_local_mac=local.port_neighbor_mac,port_status=True)
                if search.count() != 0:
                    for neighbor in search:
                        G.add_edge(ip.ipaddress,neighbor.device_ip.ipaddress)

        A = nx.nx_agraph.to_agraph(G)
        A.write('netmap.dot')

        print G.adj
