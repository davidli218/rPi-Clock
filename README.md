# Raspberry Pi Clock

A multi functional LED display clock built by Raspberry Pi.

## Feature List

- Clock
- Timer

## Hardware requirement

- Raspberry Pi
- 6 Pin 4 Digits 7 Segment LED Display (HS410361k-32)
- Buttons

## Hardware connection

### 7 Segment Display

| Segment/Digit | 7Seg Pin | Resistor | GPIO # | BCM # |
| ------------- | -------- | -------- | ------ | ----- |
| BOTTOM LEFT   | 1        | YES      | 27     | 16    |
| BOTTOM CENTER | 2        | YES      | 23     | 13    |
| DECIMAL POINT | 3        | YES      | 28     | 20    |
| BOTTOM RIGHT  | 4        | YES      | 26     | 12    |
| CENTER CENTER | 5        | YES      | 22     | 6     |
| DIGIT 4       | 6        | \        | 4      | 23    |
| Top RIGHT     | 7        | YES      | 25     | 26    |
| DIGIT 3       | 8        | \        | 3      | 22    |
| DIGIT 2       | 9        | \        | 2      | 27    |
| Top LEFT      | 10       | YES      | 24     | 19    |
| Top CENTER    | 11       | YES      | 21     | 5     |
| DIGIT 1       | 12       | \        | 1      | 18    |

### Others

| Name     | GPIO ID | BCM # |
| -------- | ------- | ----- |
| BUTTON_1 | 5       | 24    |
| BUTTON_2 | 6       | 25    |

