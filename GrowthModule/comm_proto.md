# Custom communications protocol for the Growth Modules (v1.1.0)
This protocol defines the communication between the device server running on the TLC and the ESP32 microcontroller that controls each Growth Module. It is a completely text-based protocol, so that it is flexible and easy to parse. To be transmitted, the text of the message is encoded with **utf-8**.
This protocol is an application-level protocol and runs on top of TCP/IP. The TCP port used for communication is **8503**.

The architecture is a client-server architecture. The *client* is the *device server* running on the TLC, the *server* is the program running on the ESP32. The client sends the Message, and the server sends back a Response (see Message structure below).

## Versions changelog
- v1.0.0: initial version, misses plantStates, plantTypes, GMBelowPlantStates, GMBelowPlantTypes
- v1.1.0: add missing messages

## Message structure
The general message structure is:

>message_type;cmd_or_atr_name;optional_field_values;;

The `;` acts as a field separator. The `;;` at the end indicates the end of the message.

## Encodings
The encodings are presented in the following way:
- encoded_value = meaning

When transmitting messages, `encoded_value` must be used.
  
`meaning` is what the encoding refers to.

### Booleans
If a boolean value is needed in a message below, it will be encoded as follows:
- T = True
- F = False

### Plant type : [plantiType]
- 0 = salade
- 1 = fraises
- 2 = fenouil
- 3 = chou
- 4 = radis

### Plant growth state : [plantiState]
// TODO: Confirm that these are indeed the possible growth states 
- 0 = SEEDLING
- 1 = VEGETATIVE_GROWTH
- 2 = FLOWERING
- 3 = DEVELOPMENT

## Common placeholder encodings and semantics
A placeholder in a message is written as follows: [placeholder_label]

Here, we list some common placeholders, their encodings and semantics.

- [confirmation]: value is either T or F. T means the write was successful, F means the write was unsuccessful.
- [plantiState]: is an encoded plant growth state, as defined in the Encodings section of this document.
- [LEDiState]: is either T or F. T means that LED i is on, F means that LED i is off.
- [plantiType]: is an encoded plant type. See Encodings section for encoding.
- [pumpState]: is either T or F. T means the pump is on, F means the pump is off.

## Messages

### State, Status
The State and Status commands are omitted because they are handled on the device server on the TLC. QUESTION: good idea or not?

### temperature
Message:
>atr_read;temperature;;

Response:
>atr_res;temperature;[temp];;

where [temp] is substituted by the temperature value, eg. "atr_res;temperature;23.5;;"

### pH
Message:
>atr_read;pH;;

Response:
>atr_res;pH;[pH];;

where [pH] is substituted by the pH value.

### waterLevel
Message:
>atr_read;waterLevel;;

Response:
>atr_res;waterLevel;[waterLevel];;

where [waterLevel] is substituted by the value.

### electroconductivity
Message:
>atr_read;electroconductivity;;

Response:
>atr_res;electroconductivity;[ec];;

where [ec] is the value.

### read pumpState
Message:
>atr_read;pumpState;;

Response:
>atr_res;pumpState;[pumpState];;

### write pumpState
Message:
>atr_write;pumpState;[pumpState];;

Response:
>atr_res;pumpState;[confirmation];;

### read LEDStates
Message:
>atr_read;LEDStates;;

Response:
>atr_res;LEDStates;[LED0State];[LED1State];[LED2State];[LED3State];;

### write LEDStates
Message:
>atr_write;LEDStates;[LED0State];[LED1State];[LED2State];[LED3State];;

Response:
>atr_res;LEDStates;[confirmation];;

### read plantStates
Message:
>atr_read;plantStates;;

Response:
>atr_res;plantStates;[plant0State];[plant1State];[plant2State];[plant3State];[plant4State];;

The numbers to which the plant numbers correspond are defined in the documentation of the RoboticStation
device class. For example, the following message:

>atr_res;plantStates;0;0;1;0;0;;

Means that all plants in the Growth Module are in the SEEDLING state, except plant number 2, which is in
the VEGETATIVE_GROWTH state.

### write plantStates
Message:
>atr_write;plantStates;[plant0State];[plant1State];[plant2State];[plant3State];[plant4State];;

Response:
>atr_res;plantStates;[confirmation];;

### read plantTypes
Message:
>atr_read;plantTypes;;

Response:
>atr_res;plantTypes;[plant0Type];[plant1Type];[plant2Type];[plant3Type];[plant4Type];;

### write plantTypes
Message:
>atr_write;plantTypes;[plant0Type];[plant1Type];[plant2Type];[plant3Type];[plant4Type];;

Response:
>atr_res;plantTypes;[confirmation];;


### GMBelowPlantStates, GMBelowPlantTypes
Identical to read/write plantStates, plantTypes. Only the `cmd_or_atr_name` field changes to 
GMBelowPlantStates, GMBelowPlantTypes respectively. // TODO maybe make more precise