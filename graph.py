import time
import matplotlib.pyplot as plt
from pymodbus.client import ModbusTcpClient

# Configuration du client Modbus
IP_ADDRESS = '192.168.15.1'  # Remplacez par l'adresse IP de votre serveur Modbus
PORT = 502                  # Le port Modbus standard est 502

# Créez une instance du client Modbus
client = ModbusTcpClient(IP_ADDRESS, port=PORT)

# Listes pour stocker les valeurs et les timestamps
values_0x6C = []
values_0x6D = []
timestamps = []

# Durée de la lecture et intervalle
duration = 20  # secondes
interval = 1  # secondes

# Connexion au serveur Modbus
if client.connect():
    start_time = time.time()
    while time.time() - start_time < duration:
        # Lecture des registres
        response_0x6C = client.read_holding_registers(0x6C, 1)
        response_0x6D = client.read_holding_registers(0x6D, 1)

        if not response_0x6C.isError() and not response_0x6D.isError():
            values_0x6C.append(response_0x6C.registers[0])
            values_0x6D.append(response_0x6D.registers[0])
            timestamps.append(time.time() - start_time)
        else:
            print("Erreur de lecture des registres")

        time.sleep(interval)

    # Déconnexion du client
    client.close()

    # Création du graphique
    plt.plot(timestamps, values_0x6C, label="Registre 0x6C")
    plt.plot(timestamps, values_0x6D, label="Registre 0x6D")
    plt.xlabel('Temps (s)')
    plt.ylabel('Valeur du Registre')
    plt.title('Valeurs des Registres sur le Temps')
    plt.legend()
    plt.show()

else:
    print("Échec de la connexion au serveur Modbus")
