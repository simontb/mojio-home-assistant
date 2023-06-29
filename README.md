# Mojio Home Assistant Integration
Custom component to integrate mojio with home assistant

Example configuration.yaml:

T-Mobile PL:

```yaml
device_tracker:
  - platform: mojio
    domain: tmobile-pl
    client_id: a29871cb-27c6-4e36-8249-205bafe659b3
    client_secret: 8eb2d8b3-7baf-4c41-9373-877ed9960a5f
    username: <YOUR_EMAIL_ADDRESS>
    password: <YOUR_PASSWORD>
```

T-Mobile CZ:

```yaml
device_tracker:
  - platform: mojio
    domain: tmobile-cz
    client_id: 01e950e3-5e50-4cc0-8b04-8b48c35d00cd
    client_secret: a1b7d477-9410-4e1d-b537-304e041fcb89
    username: <YOUR_EMAIL_ADDRESS>
    password: <YOUR_PASSWORD>
```

Telekom DE:

```yaml
device_tracker:
  - platform: mojio
    domain: telekom-de
    client_id: cae6e4b9-00ca-4019-be80-26ed36a30979
    client_secret: 4d37a73e-72a3-466f-8ed2-f0fd4026cb77
    username: <YOUR_EMAIL_ADDRESS>
    password: <YOUR_PASSWORD>
```

T-Mobile US (SyncUp Drive):

```yaml
device_tracker:
  - platform: mojio
    domain: tmobile-us
    client_id: 86d1d812-dc08-4d38-9ff3-ff86908d97e6
    client_secret: 0a6b21ec-84df-4088-ba0c-2e05592da42b
    username: <YOUR_EMAIL_ADDRESS>
    password: <YOUR_PASSWORD>
```



The `client_id` and `client_secret` are operator specific. It identifies the App, on the Mojio API.
