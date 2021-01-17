# Safe SJTU Backend

`The following procedures are only used for developer since everything is under construction. A tutorial will be written after major features are well accomplished.`

## How to configure the python environment

```bash
cd latest-server
# notice that python should be assigned to version 3.7 for the sake of compatibility
conda create -n <environment_name> python=3.7
conda activate <environment_name>
# install all the dependencies
pip install -r requirements.txt
```

## API (RESTful)

Since we use `Swift` (later we may deploy the service to other platforms), all the body of HTTP request and response utilize `json`.

Take a glance at the API (volatile):

```
Database: DriveS_v2
Measurement: usertable
Tag: username
Field: password_hash, public_id

Measurement: data
Tag: uuid, launch, public_id
Field: velocity, acceleration, gyroscope, latitude, longitude

API:
Route: /register
Methods: ['GET', 'POST']
Token: not required
Header:
    Authorization: <type> <credentials>
* Explanation of header authorization:
    it contains the encoded username-password pair,
    Swift provides API for this commonly used header


Route: /login
Methods: ['GET', 'POST']
Token: not required
Header:
    Authorization: <type> <credentials>

Route: /upload
Methods: ['POST']
Token: required
Header: 
    x-access-tokens: <token>
Body:
    * Same as the original version, i.e.
    * Format of request in Swift
    * let body = ["UserID":uuid,
    *             "LaunchTimestamp":LAUNCH_TIMESTAMP,
    *             "Data":uploadBuffer 
    *            ] as Dictionary<String, String>
    * Format of each line in Data in Swift
    * uploadBuffer += (Date().GetTime+",\(velocity),\(accCal[1]),\(gyroCal[2]),\(latitude),\(longitude),\n")
```

