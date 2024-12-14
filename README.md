# Xiaomi Smart Air Purifier 4 Lite MQTT Integration

## ⚠️ Warning

This project should not need to exist. However, the default installation of the Xiaomi add-on and this particular air filter does not support fan speed control. This integration uses the latest `miio` tools, which do support it but are currently in an alpha state and not directly usable in Home Assistant. Thus, this very simple and lightweight integration was created.

This project extends Home Assistant's Xiaomi integration to add MQTT-powered control for the Xiaomi Smart Air Purifier 4 Lite, enabling precise speed control through MQTT topics. This allows seamless integration and enhanced functionality within Home Assistant.

## Features

- **Full Speed Control:** Adjust fan speed via MQTT topics.
- **State Updates:** Publish the current state and speed percentage of the air purifier.
- **Home Assistant Discovery:** Automatically configure the integration in Home Assistant.
- **MQTT-Based Communication:** Lightweight and efficient control over MQTT.

## Requirements

- Xiaomi Smart Air Purifier 4 Lite
- Home Assistant
- MQTT Broker
- Python 3.10  # Required by miio tools
- Xiaomi device token and IP address (use `miio` tools to extract these)

## Setup

### Environment Variables
Create a `.env` file or set the following environment variables:

```bash
XIAOMI_IP=AIR_PURIFIER_IN
XIAOMI_TOKEN=AIR_PURIFIER_TOKEN
MQTT_HOSTNAME=YOUR_MQTT_BROKER_HOST
MQTT_PORT=1883  # Default MQTT port
MQTT_USERNAME=YOUR_MQTT_USERNAME
MQTT_PASSWORD=YOUR_MQTT_PASSWORD
MQTT_NAME_TOPIC=xiaomi-air-purifier-speed
BASE_MQTT_TOPIC=zhimi-airp-rmb1
```

### Docker Deployment
A `Dockerfile` is provided for containerized deployment. Build and run the container:

```bash
docker build -t xiaomi-air-purifier .
docker run -d --env-file .env xiaomi-air-purifier
```

### Docker-Compose Deployment
Here is a simple example of using `docker-compose` to run the integration, including `.env` file integration:

```yaml
services:
  xiaomi-air-purifier:
    build: .
    container_name: xiaomi-air-purifier
    environment:
        XIAOMI_IP: YOUR_DEVICE_IP
        XIAOMI_TOKEN: YOUR_DEVICE_TOKEN
        MQTT_HOSTNAME: YOUR_MQTT_BROKER_HOST
        MQTT_PORT: 1883  # Default MQTT port
        MQTT_USERNAME: YOUR_MQTT_USERNAME
        MQTT_PASSWORD: YOUR_MQTT_PASSWORD
        MQTT_TOPIC: xiaomi-air-purifier-speed
        BASE_MQTT_TOPIC: zhimi-airp-rmb1
    restart: unless-stopped
```

Save the above configuration in a `docker-compose.yml` file. Then, deploy the container using:

```bash
docker-compose up -d
```

### Manual Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your-repo/xiaomi-air-purifier
   cd xiaomi-air-purifier
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the script:

   ```bash
   python main.py
   ```

## MQTT Topics

| Topic                             | Description                                   |
|-----------------------------------|-----------------------------------------------|
| `zhimi-airp-rmb1/availability`    | Availability state (`online`/`offline`).      |
| `zhimi-airp-rmb1/on/state`        | Current power state (`ON`/`OFF`).             |
| `zhimi-airp-rmb1/on/set`          | Command to turn the device on or off.         |
| `zhimi-airp-rmb1/speed/percentage_state` | Current fan speed percentage (1-13).       |
| `zhimi-airp-rmb1/speed/percentage_set`   | Command to set the fan speed (1-13).       |

## Home Assistant Integration

This integration supports Home Assistant's MQTT Discovery. Once the script is running, the device will automatically appear in Home Assistant.

### Fan Configuration

The integration exposes the air purifier as a fan entity with percentage-based speed control.

## Troubleshooting

- **Device Connection Issues:** Ensure the IP and token are correct.
- **MQTT Connection Issues:** Check your broker's hostname, port, username, and password.
- **Logs:** Review logs for errors (uses `loguru` for detailed logging).

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

### Acknowledgments

This project uses the following libraries:

- [aiomqtt](https://pypi.org/project/aiomqtt/)
- [python-miio](https://pypi.org/project/miio/)
- [loguru](https://pypi.org/project/loguru/)
