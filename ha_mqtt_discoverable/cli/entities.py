from queue import Empty, SimpleQueue
from threading import Event
from paho.mqtt.client import Client, MQTTMessage, MQTT_ERR_SUCCESS
import typer

app = typer.Typer()

message_queue = SimpleQueue()


def on_mqtt_connect(client: Client, *args):
    print("Subscribing")
    result, mid = client.subscribe("homeassistant/#")
    if result != MQTT_ERR_SUCCESS:
        print("Error subscribing to MQTT topic")
        raise typer.Exit(code=1)


def on_message(client: Client, userdata: Event, message: MQTTMessage):
    print(message.topic)
    payload = message.payload.decode("utf-8")
    message_queue.put_nowait(payload)


@app.command()
def create(item: str):
    print(f"Creating item: {item}")


@app.command()
def list():
    event = Event()

    print("Listing entities")
    client = Client()
    client.on_connect = on_mqtt_connect
    client.on_message = on_message
    client.user_data_set(event)
    result = client.connect(host="localhost")
    if result != MQTT_ERR_SUCCESS:
        print("Error connecting to MQTT broker")
        raise typer.Exit(code=1)

    client.loop_start()
    finished = False
    while not finished:
        try:
            entity = message_queue.get(timeout=1)
            print(entity)
        except Empty:
            finished = True

    client.loop_stop()


@app.command()
def update(item: str):
    print(f"Updating entity: {item}")


@app.command()
def delete(item: str):
    print(f"Deleting item: {item}")
