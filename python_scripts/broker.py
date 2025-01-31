import paho.mqtt.client as mqtt

# Configuration
BROKER_ADDRESS = "localhost"  # MQTT broker address
BROKER_PORT = 1883  # MQTT broker port
TOPIC = "sensor/patient1/#"  # Topic to subscribe to

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to MQTT broker at {BROKER_ADDRESS}:{BROKER_PORT}")
        # Subscribe to the specified topic
        client.subscribe(TOPIC)
        print(f"Subscribed to topic: {TOPIC}")
    else:
        print(f"Failed to connect to MQTT broker, return code {rc}")

# Callback when a message is received
def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode("utf-8")
    print(f"Received message: Topic: {topic}, Payload: {payload}")

# Main function
def main():
    # Initialize MQTT client
    client = mqtt.Client(protocol=mqtt.MQTTv311)

    # Set up callbacks
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the MQTT broker
    print(f"Connecting to MQTT broker at {BROKER_ADDRESS}:{BROKER_PORT}...")
    client.connect(BROKER_ADDRESS, BROKER_PORT)

    # Start the MQTT client loop to process messages
    print("Listening for MQTT messages...")
    client.loop_forever()

# Run the main function
if __name__ == "__main__":
    main()

