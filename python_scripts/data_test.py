import paho.mqtt.client as mqtt
import firebase_admin
from firebase_admin import credentials, db
import os
import time
import threading

# Vérifier si le fichier existe
def check_file_exists(file_path):
    if not os.path.exists(file_path):
        print(f"Erreur : Le fichier de crédentiels '{file_path}' est introuvable.")
        return False
    return True

# Initialisation de Firebase
def init_firebase():
    try:
        credentials_file = './node-red-io-firebase-adminsdk-39qa2-7b0cda7dbb.json'
        if not check_file_exists(credentials_file):
            return None

        if not firebase_admin._apps:
            cred = credentials.Certificate(credentials_file)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://node-red-io-default-rtdb.europe-west1.firebasedatabase.app/'
            })
        print("Firebase initialisé avec succès.")
        return True
    except Exception as e:
        print(f"Erreur lors de l'initialisation de Firebase : {e}")
        return None

# Structure des données globales
data = {
    "heart_rate": [],
    "temperature": [],
    "spo2": []
}

# Gestion des messages MQTT
def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode("utf-8")
    print(f"Message reçu sur {topic} : {payload}")

    try:
        if "heart_rate" in topic:
            data["heart_rate"].append(float(payload))
        elif "temperature" in topic:
            data["temperature"].append(float(payload))
        elif "spo2" in topic:
            data["spo2"].append(float(payload))
        
        print(f"Données actuelles : {data}")
    except ValueError:
        print(f"Payload invalide : {payload}")

# Analyser les données et stocker dans Firebase
def analyze_and_store_data():
    while True:
        time.sleep(10)  # Intervalle pour collecter et analyser les données
        
        if not any(data.values()):  # Si aucune donnée n'a été collectée
            print("Aucune donnée à analyser ou à envoyer.")
            continue

        try:
            # Calculer les statistiques et détecter les anomalies
            statistics = {}
            anomalies = []

            if data["heart_rate"]:
                avg_hr = sum(data["heart_rate"]) / len(data["heart_rate"])
                max_hr = max(data["heart_rate"])
                min_hr = min(data["heart_rate"])
                statistics["heart_rate"] = {"avg": avg_hr, "max": max_hr, "min": min_hr}
                if avg_hr > 100 or avg_hr < 60:
                    anomalies.append("Anomalie : Fréquence cardiaque hors limites.")

            if data["temperature"]:
                avg_temp = sum(data["temperature"]) / len(data["temperature"])
                max_temp = max(data["temperature"])
                min_temp = min(data["temperature"])
                statistics["temperature"] = {"avg": avg_temp, "max": max_temp, "min": min_temp}
                if avg_temp > 38.0:
                    anomalies.append("Anomalie : Température élevée détectée.")

            if data["spo2"]:
                avg_spo2 = sum(data["spo2"]) / len(data["spo2"])
                min_spo2 = min(data["spo2"])
                statistics["spo2"] = {"avg": avg_spo2, "min": min_spo2}
                if avg_spo2 < 90:
                    anomalies.append("Anomalie : Saturation en oxygène faible.")

            # Afficher les anomalies détectées
            for anomaly in anomalies:
                print(anomaly)

            # Stocker les données dans Firebase
            store_data_in_firebase(statistics)

            # Réinitialiser les données après traitement
            data["heart_rate"].clear()
            data["temperature"].clear()
            data["spo2"].clear()
        except Exception as e:
            print(f"Erreur lors de l'analyse ou du stockage dans Firebase : {e}")


# Stocker les données dans Firebase avec un timestamp
def store_data_in_firebase(statistics):
    try:
        timestamp = int(time.time())  # Get the current timestamp in seconds
        ref = db.reference('/patient_data')
        ref.push({
            "timestamp": timestamp,
            "data": statistics
        })
        print(f"Données envoyées dans Firebase avec timestamp {timestamp} :", statistics)
    except Exception as e:
        print(f"Erreur lors de l'envoi des données dans Firebase : {e}")

# Démarrer le thread d'analyse et de stockage
analysis_thread = threading.Thread(target=analyze_and_store_data, daemon=True)
analysis_thread.start()

# Initialisation de Firebase et du client MQTT
if init_firebase():
    print("Firebase initialisé. Démarrage du client MQTT...")
else:
    print("Échec de l'initialisation de Firebase. Sortie.")
    exit(1)

broker_address = "localhost"
client = mqtt.Client(protocol=mqtt.MQTTv311)

# Gestion de la connexion MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connecté au broker MQTT avec succès.")
    else:
        print(f"Échec de la connexion au broker MQTT, code de retour {rc}")

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address)
client.subscribe("sensor/patient1/#")

print("En attente de messages MQTT...")
client.loop_forever()
