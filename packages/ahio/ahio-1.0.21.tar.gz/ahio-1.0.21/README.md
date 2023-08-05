ahio
====

ahio is a communication library whose goal
is to abstract the interfacing with various I/O hardwares, so that changing
hardware becomes possible with minimum code modification. It's desired that
an application that already works with an I/O hardware will only need pin
remapping and possibly initial setup change to work with another hardware, not
entire code rewrite.

It works with drivers, which are installed in the `ahio.drivers` package. Every
driver must implement the API described in the `ahio.abstract_driver` package.
If you plan to use this library or develop a driver, read the documentation
there.


Installation
------------

Simplest way is to use pip: `pip3 install ahio`
Alternatively you can checkout this repository and run
`python3 setup.py install`


Basic usage
-----------

```python
# Import the package:
import ahio

# You can see what drivers are available in this platform by calling
print(ahio.list_available_drivers())

# Instantiate the desired driver
with ahio.new_driver('Arduino') as arduino:
  # The driver can have a driver-specific setup function. Call it as/if needed.
  arduino.setup('/dev/tty.usbmodem1421')

  # Map the pins. From now on, when you use 1 in the API, it will have effects
  # on pin D3 in the Arduino. If you change hardware in the future, just change
  # the mapping.
  arduino.map_pin(1, arduino.Pins.D3)
  arduino.map_pin(2, arduino.Pins.D13)
  arduino.map_pin(3, arduino.Pins.A1)

  # Change a pin direction (Input or Output)
  arduino.set_pin_direction([1, 2], ahio.Direction.Output)
  arduino.set_pin_direction(3, ahio.Direction.Input)

  # Set the output of a pin
  arduino.write([1, 2], ahio.LogicValue.High)
  arduino.write(1, 0.4, pwm=True)

  # Read the input of a pin
  print(arduino.read(3))
```

Documentation
-------------

Documentation is hosted at [GitHub](https://acristoffers.github.io/ahio)
