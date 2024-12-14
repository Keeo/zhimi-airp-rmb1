import asyncio
import json
import os
from asyncio import sleep
from typing import Union
from aiomqtt import Client, Will
from loguru import logger
from miio import DeviceFactory, AirPurifierMiot, Device

MQTT_NAME_TOPIC = os.getenv("MQTT_NAME_TOPIC", "xiaomi-air-purifier-speed")
MQTT_BASE_TOPIC = os.getenv("BASE_MQTT_TOPIC", "zhimi-airp-rmb1")

DISCOVERY_TOPIC = f"homeassistant/fan/{MQTT_NAME_TOPIC}/config"

AVAILABILITY_TOPIC = f"{MQTT_BASE_TOPIC}/{MQTT_NAME_TOPIC}/availability"
STATE_TOPIC = f"{MQTT_BASE_TOPIC}/{MQTT_NAME_TOPIC}/on/state"
COMMAND_TOPIC = f"{MQTT_BASE_TOPIC}/{MQTT_NAME_TOPIC}/on/set"
PERCENTAGE_STATE_TOPIC = f"{MQTT_BASE_TOPIC}/{MQTT_NAME_TOPIC}/speed/percentage_state"
PERCENTAGE_COMMAND_TOPIC = f"{MQTT_BASE_TOPIC}/{MQTT_NAME_TOPIC}/speed/percentage_set"


async def main():
    device: Union[AirPurifierMiot, Device] = DeviceFactory.create(
        os.getenv("XIAOMI_IP"),
        os.getenv("XIAOMI_TOKEN"),
    )

    async def publish_speed():
        payload = device.status().favorite_level - 1
        logger.info(f"Publishing speed at {PERCENTAGE_STATE_TOPIC=} with '{payload=}'")
        await client.publish(
            PERCENTAGE_STATE_TOPIC,
            payload,
            retain=True,
        )

    async def publish_state():
        payload = "ON" if device.status().is_on else "OFF"
        logger.info(f"Publishing state at {STATE_TOPIC=} with '{payload=}'")
        await client.publish(
            STATE_TOPIC,
            payload,
            retain=True,
        )

    async def update():
        while True:
            logger.info(f"Will check if anything changed and update accordingly")
            await publish_state()
            await publish_speed()
            await sleep(60)

    async def listen():
        async for message in client.messages:
            if message.topic.matches(COMMAND_TOPIC):
                payload = message.payload.decode()
                if payload == "ON":
                    device.on()
                elif payload == "OFF":
                    device.off()
                else:
                    logger.error(f"Unknown message payload: {payload}")

                await publish_state()

            if message.topic.matches(PERCENTAGE_COMMAND_TOPIC):
                payload = message.payload.decode()
                try:
                    speed = int(payload)
                    if speed < 14:
                        speed += 1

                    logger.info(f"Setting fan speed to {speed}")
                    device.set_favorite_level(speed)

                    await publish_speed()
                except ValueError as e:
                    logger.error(f"Invalid payload: {payload=} {e=}")

    async with Client(
        hostname=os.getenv("MQTT_HOSTNAME"),
        port=int(os.getenv("MQTT_PORT", "1883")),
        username=os.getenv("MQTT_USERNAME"),
        password=os.getenv("MQTT_PASSWORD"),
        will=Will(topic=AVAILABILITY_TOPIC, payload="offline", qos=1),
    ) as client:
        logger.info(f"Subscribing to {COMMAND_TOPIC=} and {PERCENTAGE_COMMAND_TOPIC=}")
        await client.subscribe(COMMAND_TOPIC)
        await client.subscribe(PERCENTAGE_COMMAND_TOPIC)

        logger.info(f"Publishing availability at {AVAILABILITY_TOPIC=}")
        await client.publish(
            AVAILABILITY_TOPIC,
            "online",
            qos=1,
        )

        discovery_payload = {
            "name": "Xiaomi Smart Air Purifier 4 Lite",
            "unique_id": device.device_id,
            "command_topic": COMMAND_TOPIC,
            "state_topic": STATE_TOPIC,
            "availability_topic": AVAILABILITY_TOPIC,
            "percentage_command_topic": PERCENTAGE_COMMAND_TOPIC,
            "percentage_state_topic": PERCENTAGE_STATE_TOPIC,
            "speed_range_min": 1,
            "speed_range_max": 13,
            "qos": 1,
            "device": {
                "identifiers": [device.info().mac_address],
                "manufacturer": "Xiaomi",
                "model": device.info().model,
            },
        }
        logger.info(
            f"Publishing discovery payload at {DISCOVERY_TOPIC=} values: {discovery_payload=}"
        )
        await client.publish(
            DISCOVERY_TOPIC, json.dumps(discovery_payload), retain=True
        )

        logger.info(f"All set, starting to listen")
        try:
            await asyncio.gather(
                listen(),
                update(),
            )
        except Exception as e:
            logger.exception(f"Something broke, will exit and un alive {e}")
            await client.publish(
                AVAILABILITY_TOPIC,
                "offline",
                qos=1,
            )
            raise


if __name__ == "__main__":
    asyncio.run(main())
