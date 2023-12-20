import time
from pymodbus.client import ModbusTcpClient
from constant import Register

# Configuration du client Modbus
IP_ADDRESS = '192.168.15.1'  # Remplacez par l'adresse IP de votre serveur Modbus
PORT = 502                  # Le port Modbus standard est 502

# Configuration du registre
register = Register()

# Créez une instance du client Modbus
client = ModbusTcpClient(IP_ADDRESS, port=PORT)

# Connexion au serveur Modbus
if client.connect():
    print("Connecté au serveur Modbus")

    try:
        while True:  # Boucle infinie
            # Écriture de la valeur 100 dans le registre order_rub
            client.write_register(register.phy_l_rub, 100)
            client.write_register(register.phy_r_rub, 100)
            print("Valeur 100 écrite dans le registre 0x0028")

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Arrêt du script par l'utilisateur")

    finally:
        # Déconnexion du client
        client.close()
        print("Déconnecté du serveur Modbus")

else:
    print("Échec de la connexion au serveur Modbus")
