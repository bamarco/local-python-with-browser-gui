# Local Deployment of a Python Application with Browser Based GUI
Suppose we are building a **Python Application** that needs to run **Locally** (i.e. without internet access). We may still want to use an internet browser for the Graphical User Interface (**GUI**). A **Browser Based GUI** has access to the browser's rich ecosystem that is difficult to compete with. 

The Application will consist of:

- [Backend Core](#backend-core) – core capabilities written in python 
- [Backend API](#backend-api) – API library and glue code
- [Frontend](#frontend) – Browser Based GUI

To deploy the Application we will need:

- [Runtime](#runtime) – environment in which the Application will run
- [Build System](#build-system) – system for compiling the Application

Let's explore alternative approaches for creating such an Application.

## Backend Core
For the purposes of this evaluation, we will assume the backend capabilities have already been written. As stand-ins for these capabilities we provide [backend.py](backend.py) which contains some simple demonstration functions.

## Backend API
To access the capabilities of the Backend Core, we will need an Application Program Interface (**API**) to communicate with the Frontend. We will narrow our API search to REpresentational State Transfer (**REST**) and Remote Procedure Calls (**RPC**).

REST:

- [Flask](#flask)
- [Fastapi](#fastapi)

RPC:

- [gRPC](#grpc)
- [ZeroRPC](#zerorpc)
- [ZMQRPC](#zmqrpc)

For a broader overview of API choices read [An architect's guide to APIs: SOAP, REST, GraphQL, and gRPC](https://www.redhat.com/architect/apis-soap-rest-graphql-grpc) and [What is the current choice for doing rpc in python](https://stackoverflow.com/questions/1879971/what-is-the-current-choice-for-doing-rpc-in-python).

### Flask
[Flask](https://flask.palletsprojects.com/en/3.0.x/) is a large, popular web framework for python. The tradeoffs are typical of popular frameworks.

- [app.py](app.py)

#### Positives
- lots of features
- documentation is ubiquitous
- most edge cases have already been addressed 
- easier to find developers already familiar with it
- code can be reused for web deployment

#### Negatives
- lots of features                                |
- heavyweight (especially for a local deployment) |

### Fastapi
- https://fastapi.tiangolo.com/

### gRPC
- https://grpc.io/docs/languages/python/

#### Positives
- faster
- smaller

#### Negatives
- less established
- less features 

### ZeroRPC
- https://github.com/0rpc/zerorpc-python

### ZMQRPC
- https://github.com/geoffwatts/zmqrpc

## Frontend 
There are many toolsets available to produce Browser Based GUIs. The [Javascript Framework](#javascript-framework) crowd use frameworks like Angular, React, Vue, etc, etc, etc. The [Vanilla Javascript](#vanilla-javascript) proponents prefer a simpler approach, eschewing frameworks altogether and using javascript directly. [HTMX](#htmx) proponents propose an even simpler approach, eschewing javascript altogether[^1] and instead extending HTML. There are those who prefer a low-level graphics approach; they use WebGL and/or Web Assembly (**WASM**) to produce interfaces without the Document Object Model (**DOM**). [Flutter](#flutter) and [eGUI](#egui) are two such examples.


### Javascript Framework
There are many established javascript frameworks available. For brevity we only explore [Vue](https://vuejs.org).

For instructions on running the Vue frontend see [frontend/README.md](frontend/README.md).

#### Positives
- Lots of libraries
- Established Documentation 
- Most edge cases are already addressed 

#### Negatives
- Heavyweight 
- Additional build steps 

### Vanilla Javascript

#### Positives
- Lightweight
- Easier to debug code we wrote ourselves 

#### Negatives
- Fewer libraries
- More code to write ourselves 
- Has a tendency to turn into a poorly planned framework

### HTMX
HTMX is currently implemented as a small javascript library. We use little to no javascript ourselves when using HTMX. HTMX extends HTML with a few small capabilities that give all elements the abilities of forms and hrefs.

#### Positives 
- Lightweight
- Most Application logic can stay in python 

#### Negatives
- Less capability for rich interface
- Charts/Graphs less integrated
- Newer with more undocumented edge cases

### Flutter
The tooling is currently a dealbreaker. Depending on proprietary build tools is a disaster waiting to happen, so we'll skip this one.

#### Positives
- Highly cross-platform
- GUI representations are artist friendly (e.g. no div)

#### Negatives
- Complex build/tooling tightly integrated with Android

### eGUI
eGUI is an immediate mode GUI written in Rust. Unlike retained mode that most GUI use, we recreate the user interface every frame as in video games. 

#### Positives
- Possible to make richer interfaces 
- GUI representations are artist friendly (e.g. no div)
- Simplicity of immediate mode
- Runtime speed

#### Negatives
- More difficult to implement accessiblity support 
- Low number of prebuilt libraries 


## Runtime
The runtime will have a large impact on the ease of installation, ease of use, and complexity of the user interface.

The typical user of an Application is unaware of the split between Backend and Frontend. Such users consider the GUI to be the entirety of the Application. Some runtimes hide the split better than others. Even for power users, splitting the Application into two parts can be cumbersome.

We can have an Application that runs completely standalone, completely within the browser, or split between the two:

- [Simulated Native Application](#simulated-native-application) – completely standalone; executable includes entire runtime for the Frontend
- [Progressive Web Application](#progressive-web-application) – completely in the browser Backend runs on WASM
- [Service Backend](#service-backend) – Backend runs standalone, Frontend runs in the browser
- [From Source](#from-source) – Uses the source code and the python runtime to run the Backend; best for development

### Simulated Native Application
A Simulated Native Application opens no differently than a native application. The Application itself will not match the style of the host operating system which can cause some minor annoyances and confusion.

[Electron](https://www.electronjs.org/) acheives this style by shipping an entire internet browser, but is less than ideal in terms of size and complexity.

Some web assembly runtimes (e.g. WASMER) may have the capability to run a standalone Frontend. Requires further investigation.

### Progressive Web Application
A Progressive Web Application opens no differently than a typical online web application. This is a nice experience, but may take additional steps to convince users that the applicaiton runs without needing interet access. Progressive Web Applications are relatively new and may require complex build steps and increased development time to acheive.

Technologies:

- Emscripten
- Pyodide
- rattler
- WASM

### Service Backend
Types of deployment for a Service Backend:

- [Executable Service](#executable-service) – Backend is required to handle its own lifetimes while running
- [Containerized Service](#containerized-service) – Backend requires a container platform to run
- [WASM Service](#wasm-service) – Backend requires a dedicated WASM runtime to run
- [OS Service](#os-service) – Backend requires the Operating System to run it in the background


#### Exectuable Service
Windowed:
Starting the Backend also displays a Backend Window. The Backend Window will direct the user to the browser where the Frontend resides. When the Backend Window is closed the Backend stops and the Frontend no longer function. The frontend should detect when the backend is closed and direct the user to restart the backend if it cannot do so automatically.

Within Secondary Application:
Starting the backend 

Websocket/Polling with Timeouts:
The Backend closes when no more tabs are open in the application. It will communicate with the Frontend to determine when all instances of the Frontend have closed, at which point it will shutdown. The frontend should detect when the backend is shutdown and direct the user to restart the backend if it cannot do so automatically.

#### Containerized Service
The user will need to install and become familar with tools such as Docker or Podman. These tools are typically designed for more technical users. The Backend and Frontend will need to be started separately. 

#### WASM Service
There are non-browser based runtimes that can run WASM based appliations such as WASMER. The user will need to install one of these runtimes. A strategy for displaying the Frontend will still be needed. It may be possible to acheive Simulated Native Application Style.

#### OS Service
Use modern operating system services (such as systemd) to manage the backend and allow the frontend to connect. The user will either need to take more responsiblity for the running service or the service will need to run unnecessarily when not in use. The frontend will still need to be opened somehow presumably along the lines of a Simulated Progressive Web Application. 

### From Source
Use python to run the source code directly.

We can use a python [Virtual Environment (venv)](https://docs.python.org/3/library/venv.html) using the default python packaging system [pip](https://pypi.org/project/pip/).

#### Linux/OSX
``` sh
python -m venv .venv
```

``` sh
source .venv/bin/activate
```

#### Windows
We'll have a better time if we install a recent version of [powershell](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.4)
``` sh
python -m venv venv
```

``` sh
.\venv\Scripts\activate
```

## Build System

Technologies:
- Shell Script
- Pyinstaller
- Nix/Guix Universal Build System
- Github Actions
- Using the Zig Build System


[^1]: HTMX actually still uses javascript 
