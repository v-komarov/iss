#coding:utf8

from django.core.management.base import BaseCommand, CommandError
from iss.equipment.models import devices_ip
import networkx as nx
import pickle
import matplotlib.pyplot as plt


class Command(BaseCommand):
    args = '<graph ...>'
    help = 'saving graph'




    def handle(self, *args, **options):

        G = nx.Graph()

        for ip in devices_ip.objects.all():

            G.add_node(ip.ipaddress,shape='box',name=ip.device_name,location=ip.device_location,descr=ip.device_descr,label="\N\nlocalion:%s\ndescr:%s\nname:%s" % (ip.device_location,ip.device_descr,ip.device_name))
            if len(ip.lldp_neighbor_mac) !=0:
                for item in devices_ip.objects.filter(lldp_neighbor_mac__contains=[ip.chassisid]):
                    G.add_edge(ip.ipaddress,item.ipaddress)

        #L = pickle.dumps(G)

        A = nx.nx_agraph.to_agraph(G)
        A.write('netmap.dot')


        #print G.adj

        nx.draw(G)
        plt.savefig("net.png")

        #print nx.clustering(G)