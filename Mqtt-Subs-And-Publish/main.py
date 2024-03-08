import paho.mqtt.client as mqtt
from time import sleep

host = "mqtt.eclipse.org"
port = 1883
username = "usernames"
password = "password"
topic = "topic/test"


# Callback respon connect to broker MQTT
def on_connect(client, userdata, flags, rc):
    print("Connect to MQTT :", str(rc))
    client.subscribe(topic)


# Callback message from broker
def on_message(client, userdata, msg):
    print("Received a message !")
    print(f"Topik: {msg.topic}; Pesan: {str(msg.payload.decode("utf-8"))}")


if __name__ == "__main__":
    client = mqtt.Client()  # init Mqtt client
    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set(username, password)
    client.connect(host, port, 60)
    client.on_message = on_message
    client.publish(topic, "Ini adalah pesan pertama")  # test publish message
    client.loop_stop()
    client.disconnect()
    sleep(1)
