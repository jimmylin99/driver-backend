# safesjtu-backend

`The following procedures are only used for developer since everything is under construction. A tutorial will be written after major features are well established.`

### How to configure the python environment

```bash
cd latest-server
# notice that python should be assigned to version 3.7 for the sake of compatibility
conda create -n <environment_name> python=3.7
conda activate <environment_name>
# install all the dependencies
pip install -r requirements.txt
```

### Structure

Though the repo name implies it contains backend codes, we also put some light-weight frontend codes here. The repo mainly serves three jobs: 

* data collection & storage;
* labeling (including frontend)
* visualization for algorithm

The infrastructure of the backend includes (while not all of the following parts are directly related to code in this repo):

* supervisor
* nginx
* gunicorn
* flask
* influxdb
* grafana

The API to communicate with client (or say frontend in the web fashion) are divided into two parts shown in the following sections.

### How to modify the algorithm and visualize it?

Since the algorithm may be reused and tested in different sections by different developers, we decided to distribute it into a stand-alone repo `safesjtu-algo`. While this is a great idea to decouple different tasks, it introduces some advanced operation related to `git`.

#### git submodule

To run the algorithm from the (backend) server, traditionally we need to copy files in the algorithm repo into this backend repo, which is ugly and contradictory to our original intention. Thanks to `git`, it provides `git submodule` mechanism.

We treat the `safesjtu-algo` repo as a submodule in this `safesjtu-backend` repo, as clearly stated in `.gitmodules` file. If you are interested in the details, it is free to read the official documentation; otherwise, you can just follow the following procedure to (hopefully) deal with the synchronization issues.

To modify the algorithm, please clone the `safesjtu-algo` repo, and do the modification in your local git environment as usual. After a (seemingly) stable modification, you need to push your local `safesjtu-algo` repo to the corresponding remote branch. All of the above procedures have no relation to this `safesjtu-backend` repo.

Then you need to connect to `safesjtu` server, either via terminal or VSCode (I personally recommend you use VSCode SSH plugin to handle this). You need to move to the `safesjtu-backend` repo before moving on.

Just type

```bash
git submodule update --remote
```

it will synchronize the `safesjtu-algo` repo with the submodule in `safesjtu-backend` repo.

* Notice that the URL for the submodule uses https, so you may be asked for username and password (if you do not use VSCode SSH plugin). Although using password directly is allowed before late 2021, it is highly recommended to use Github personal token instead.

So far, we have accomplished most of the work for a single algorithm update (although this tutorial writes a lot, it is rather simple after you accomplished it once). The last step is to take it into effect.

Just visit the URL `https://supervisor-safesjtu.acemap.cn`, click `restart`.

### API for data input and output

The URL will in the form of `https://datainput-safesjtu.acemap.cn/<rest_api>`.

Since we use `Swift` and `Wechat App`, we resort to Restful API and hence utilize `json`.

Let's take a glance at the APIs (volatile):

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

### API for visualization

The URL will in the form of `https://datainput-safesjtu.acemap.cn/<api>`.

The response will be in rich html format, so please use modern web browser to view them.

```
Route: /replay
Methods: ['GET']
Token: not required
Header: no additional info is required
Body: no additional info is required

Route: /algo-test
Methods: ['GET']
Token: not required
Header: no additional info is required
Body: no additional info is required
```

