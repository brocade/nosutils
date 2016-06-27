from docker import Client
from prettytable import PrettyTable
from CLI import CLI 
import sys


class  DockerClient:
    def __init__(self,ip,dname):
        self.cli = Client(base_url='tcp://' + ip + ':4000')

    def format_mac(mac: str) -> str:
         mac = re.sub('[.:-]', '', mac).lower()
         mac = ''.join(mac.split())
         mac = ".".join(["%s" % (mac[i:i+4]) for i in range(0,12,4)])
         return mac

    def fetch_containers(self):
        self.containers =  self.cli.containers(trunc=False)
        if (dname=="test"):
            print("success")

    def parse_containers(self):
        self.container_map = {}
        for container in self.containers:
            cont = {}
            cont['Name'] = container['Names'][0]
            cont['IP'] = container['IP']
            cont['Image'] = container['Image']
            cont['status'] = container['Status']
            self.container_map[cont['Name']] = cont


    def fetch_networks(self):
        self.networks = self.cli.networks()

    def parse_networks(self):
        containers = []
        for net in self.networks:
            driver = net['Driver']
            if(driver==dname):
                net_name = net['Name']
                net_containers = net['Containers']
                for cont_id,cont in net_containers.iteritems():
                    container = {}
                    container ['Id'] = cont_id
                    if container['Id'].startswith('ep-'):
                       continue
                    container ['Name'] = cont['Name']
                    container ['IPv4Address'] = cont['IPv4Address']
                    container ['MacAddress'] =  cont['MacAddress']
                    container ['Network'] = net_name
                    container ['EndpointId'] = cont['EndpointID']
                    cmap = self.container_map[cont['Name']]
                    for item, cont_info in cmap.iteritems():
                         container['HostName'] = cont_info['IP']
                    fmt_mac = format_mac(cont['MacAddress'])
                    showmac = CLI("show mac-address-table address {}".format(fmt_mac))
                    found = 0
                    for item in showmac.get_ouput():
                         if "VlanId" in item:
                            continue
                         elif "Total" in item:
                            continue
                         else:
                             found = 1
                             mac_split = item.split()
                             ifname = mac_split[4] + " " + mac_split[5]
                             container['SwitchInterface'] = ifname
                             containers.append(container)

        self.parsed_containers = containers

    def printTable(self):
        x = PrettyTable(["Name", "Network", "Host Name", "Switch Interface", "IPv4Address", "MacAddress"])
        x.align = "l" 
        x.padding_width = 1

        for cont in self.parsed_containers :
            x.add_row([cont['Name'],cont['Network'],cont['HostName'],
                  cont['SwitchInterface'], cont['IPv4Address'],cont['MacAddress']])

        print(x)
        print('Done')


dc = DockerClient(sys.argv[1], sys.argv[2])
dc.fetch_containers()
dc.parse_containers()
dc.fetch_networks()
dc.parse_networks()
dc.printTable()







