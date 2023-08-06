# FiberPI
Package that automates detecting contaminated fiber connectors between switches using the switch CLIs.

## Installation

```bash
pip install FiberPI
```

## Usage
```python
import FiberPI as FPI

#Create the two switches
ubnt = FPI.node('Ubiquiti', '192.168.1.1', 'ubiquiti_edgeswitch', 'user', 'pass')
dlink = FPI.node('D-Link', '192.168.1.2', 'dlink_dgs', 'user', 'pass')

#Create the connection using a context manager to open and close connections
with FPI.connection('conn', ubnt, dlink, 1, 27, 0, 1, 1) as conn:
    #Detect Contamination
    result = conn.DetectContamination()
```
## Contributing
Anyone is welcome to contribute, if you'd like send a pull request for major changes with the changes you'd like to make.

## License
[MIT](https://choosealicense.com/licenses/mit/)
