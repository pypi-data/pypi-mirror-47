# POTNANNY-CORE
Python Package that contains all core models, schemas, db interfaces, and utilities for the PotNanny Raspberry Pi application.

See the main [PotNanny](https://github.com/jeffleary00/potnanny) project for more details and documentation.

## INSTALL AND INITIALIZE DATABASE
```
pip3 install potnanny-core
potnanny db init
```

## SAMPLE CLI COMMANDS

### POLL DEVICES FOR MEASUREMENTS
```
potnanny poll
potnanny poll --force
```

### SCAN BLE DEVICES
```
potnanny ble scan
```

### LIST ROOMS
```
potnanny room list
```

### ADD A ROOM
```
potnanny room add "my room"
```

### RENAME ROOM(id)
```
potnanny room rename 1 "new room name"
```

### ENVIRONMENT READINGS FROM ALL ROOMS
```
potnanny room read
```

### LIST ROOM ON-OFF SCHEDULES
```
potnanny room schedules 1
```

### LIST SENSORS
```
potnanny sensor list
```

### RENAME SENSOR(id)
```
potnanny sensor rename 1 "new sensor name"
```

### ASSIGN SENSOR(id) TO ROOM(id)
```
potnanny sensor assign 3 1
```

This is just an example of some of the CLI commands. See ```potnanny --help``` for more details.


## CONTACT
potnanny@gmail.com
