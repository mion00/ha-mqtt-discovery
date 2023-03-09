import typer

from ha_mqtt_discoverable.cli import entities


app = typer.Typer()
app.add_typer(entities.app, name="entities")

# @app.callback()
# def callback():
#     """
#     Home Assistant MQTT discoverable
#     """
