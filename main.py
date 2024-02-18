import nmap
from getmac  import get_mac_address 
from telegram import Bot
import asyncio

IP = '<Your IP>' # Your router/default address.
KNOWN_DEVICES = ['<list of all known devices>']

TELEGRAM_BOT_TOKEN = '<bot token from telegram>'

CHAT_ID = '<chat id from telegram>'

    
    def __init__(self, ip:str):
        self.ip = ip
        self.connected_devices = set()

    def scan(self):
        network = f"{self.ip}/24"
        nm = nmap.PortScanner()

        while True:
              nm.scan(hosts=network, arguments="-sn")
              host_list = nm.all_hosts()

              for host in host_list:
                   mac = get_mac_address(ip=host)
               #     print(mac)

                   if mac and mac not in self.connected_devices and mac not in KNOWN_DEVICES:
                        print("new device found")
                        self.notify_new_devices(mac)
                        self.connected_devices.add(mac)


    async def send_telegram_message(self,bot,chat_id,message):
         await bot.send_message(chat_id=chat_id,text=message)


    def notify_new_devices(self,mac):
         bot  = Bot(token=TELEGRAM_BOT_TOKEN)
         nmp = nmap.PortScanner()
         machine = nmp.scan(IP, arguments='-O')
         asyncio.run(self.send_telegram_message(bot,CHAT_ID,message=f"New Device Found !! MAC ADDRESS IS: {mac} and device type is: {machine['scan'][IP]['osmatch'][0]['osclass'][0]['osfamily']}"))
                   




if  __name__ == "__main__":
     scanner  = NetworkScanner(IP)
     scanner.scan()