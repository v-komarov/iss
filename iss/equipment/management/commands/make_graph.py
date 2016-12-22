#coding:utf8

from django.core.management.base import BaseCommand, CommandError
from iss.equipment.models import devices_ip,agregators
import networkx as nx
import pickle
import matplotlib.pyplot as plt


class Command(BaseCommand):
    args = '<graph ...>'
    help = 'saving graph'




    def handle(self, *args, **options):


        #### ip aдреса агрегаторов
        aip = set()

        #### mac-и  - которые необходимо исключить
        macoff = []


        #### Список агрегаторов с uplink-ами
        for ag in agregators.objects.all():

            aip.add(ag.ipaddress)

            if devices_ip.objects.filter(ipaddress=ag.ipaddress,device_domen=ag.domen).count() == 1:
                d = devices_ip.objects.get(ipaddress=ag.ipaddress,device_domen=ag.domen)
                for item in d.ports["ports"]:
                    if item["port"] in ag.uplink_ports:
                        macoff.append(item["mac"])


        #print macoff

        G = nx.Graph()

        for ip in devices_ip.objects.all():

            G.add_node(ip.ipaddress,shape='box',name=ip.device_name,location=ip.device_location,descr=ip.device_descr,label="\N\nlocalion:%s\ndescr:%s\nname:%s" % (ip.device_location,ip.device_descr,ip.device_name))
            if len(ip.lldp_neighbor_mac) !=0 and ip.lldp_neighbor_mac not in macoff and ip.chassisid not in macoff:
                #### Проверка uplink-ов
                for item in devices_ip.objects.filter(lldp_neighbor_mac__contains=[ip.chassisid]):
                    G.add_edge(ip.ipaddress,item.ipaddress)

        ### Набор не соединенных графов
        agr_graph = nx.connected_components(G)

        ### Поиск "своих" графов для агрегаторов
        a = '10.10.187.1'

        for g in agr_graph:
            if a in g:
                print type(a)
                print g
                #agr = agregators.objects.get(ipaddress=a)
                #data = agr.data
                #data["by_lldp_graph"] = pickle.dumps(g)
                #agr.data = data
                #agr.save()

        #L = pickle.dumps(G)

        ##A = nx.nx_agraph.to_agraph(G)
        ##A.write('netmap.dot')


        #print G.adj

        ##nx.draw(G)
        ##plt.savefig("net.png")

        #print nx.clustering(G)
