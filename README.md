# Send and Receive Messages via MQTT

You will implement a client to send structured data to a server. You will also implement a client that will receive the structured data.

You will create three separate files for this lab: a subscriber, a publisher, and a utility component.

### Util

This file will have the following:

1. A `start_id` that will be initially set to 111 or your favourite number. This will be used to number the payload.
2. A `create_data()` function that will create and return a dict. This will be the payload.
3. A `print_data()` function that will take a dict and print the parts in a human-readable format.

The following is a sample of the data I used. You should not use mine; you must come up with something of comparable complexity.

```python
{
    'id': 112,  # sequence number
    'patient': patient,  # name of patient
    'time': time.asctime(),  # time this was generated
    'heart_rate': int(random.gauss(80, 1)),  # heart rate
    'respiratory_rate': int(random.gauss(12, 2)),  # respiratory rate
    'heart_rate_variability': 65,  # ???
    'body_temperature': random.gauss(99, 0.5),  # temperature
    'blood_pressure': {  # subkey
        'systolic': int(random.gauss(105, 2)),  # systolic pressure
        'diastolic': int(random.gauss(70, 1))  # diastolic pressure
    },
    'activity': 'Walking'  # activity
}
```

We can use a class to model our data, but that would be overkill. Maybe a Python dataclass would be a better fit. However, a Python dictionary is able to satisfy all of our needs and it is also lightweight.

### Publisher

This file will have the following:

1. Call the above function to obtain a dict.
2. Convert the above dict to a string. Use `json.dumps()`.
3. Create a client.
4. Connect to the server.
5. Publish to the server.
6. Print a message.
7. Close the connection.

It might be advisable to do the above a number of times while sleeping at the end of each cycle.

### Subscriber

This file will have the following:

1. Create a client.
2. Assign the `on_message` delegate to the function in Step 7.
3. Connect to the server.
4. Subscribe to the required topic.
5. Print a message.
6. Invoke the client `loop_forever()` method.
7. Create a function to do the following (see signature in text or ppt slide):
    - Decode the message.
    - Convert the decoded string to a dict. Use the `json.loads()` function.
    - Call the function in the first file to print the dictionary.

## Due

See schedule for due date.

### Submission

1. You will follow the normal naming pattern for your code file, e.g., `group_«your_group_number»_util.py` (e.g., `group_1_util.py`).
2. Must be uploaded to course dropbox.

### Rubrics

Here is the corrected table with the numbers in the second column:

| Util                              | Count   |
|-----------------------------------|---------|
| \[Start ID\]                      | 1/1     |
| \[Create Data\]                   | 8/8     |
| \[Print Data\]                    | 3/3     |
| \[Coding Style\]                  | 2/2     |
| **Sub-total**                     | **14/14**|
| Publisher                         |         |
| \[Call Create Data\]              | 2/2     |
| \[Convert Payload to String\]     | 2/2     |
| \[Create Client\]                 | 2/2     |
| \[Connect to Server\]             | 2/2     |
| \[Publish\]                       | 1/1     |
| \[Print Feedback\]                | 1/1     |
| \[Close Connection\]              | 1/1     |
| \[Repeat\]                        | 2/2     |
| **Sub-total**                     | **13/13**|
| Subscriber                        |         |
| \[Create Client\]                 | 2/2     |
| \[Wire Up Handler\]               | 2/2     |
| \[Connect to Server\]             | 2/2     |
| \[Subscribe to Topic\]            | 1/1     |
| \[Print Message\]                 | 1/1     |
| \[Invoke the Loop Forever\]       | 1/1     |
| \[Handler: Decode Message\]       | 2/2     |
| \[Handler: Convert to Dict\]      | 1/1     |
| \[Handler: Print Message\]        | 1/1     |
| **Sub-total**                     | **13/13**|
| **Total**                         | **40/40**|

## Appendix

`utils.py`

```python
# author : Narendra
# date   : November 22, 2021
#filename: wk12a_utils.py
#

#data format:
# id: 111
# time: 
# person: {
#  name: 'Narendra'
#  cell: '123-456-789'
# }
# core_temp: 98
# 
from random import randint
from time import asctime
from json import dumps

class Util:
    def __init__(self):
        self.start_id = 111
        self.temp = 37
        self.person = {'name':'Nataliia', 'cell': '(123)456-7890'}

    def get_json_data(self):
        self.start_id += 1
        self.temp += randint(-10, 10) /1000
        data = {'id': self.start_id, 'time': asctime(), 'core_temp': self.temp, 'person': self.person}
        return dumps(data, indent=2)

# gen = Util()
# for x in range(5):
#     print(gen.get_json_data())
```
