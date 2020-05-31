# Docker HomeAssistant camera image uploader over FTP
![Docker Build](https://github.com/pilotak/docker-hass-camera-ftp/workflows/Docker%20Build/badge.svg)

```yaml
version: "3.6"
services:
  uploader:
    container_name: uploader
    restart: always
    image: pilotak/hass-camera-ftp
    environment:
      - CAMERA_COMPONENT=camera.my_camera_name
      - HEADING_SENSOR=sensor.heading
      - HASS_URL=http://192.168.88.5:8123
      - TOKEN=abcdefghijklmnopqrstuvwxyz
      - SEND_INTERVAL=60
      - FTP_HOST=test.com
      - FTP_USER=user
      - FTP_PASSWORD=password
      - FTP_REMOTE_PATH=/camera/
      - FTP_REMOTE_FILE=image.jpg
```