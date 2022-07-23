<div id="top"></div>

# Inventory Management in a Logistics Distribution Network through Reinforcement Learning


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ul>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#project-organization">Project Organization</a></li>
  </ul>
</details>



## About The Project

This repository contains the results of my bachelors thesis on the application of reinforcement learning in logistics distribution networks and inventory management. The project was implemented in python. The focus of this project was on the creation of an openAI Gym reinforcement learning environment containing a distribution network simulation. The implementation of different features was done in an iterative approach with frequent testing of the environment through common reinforcement learning agents from Stable-Baselines.

### Used Libraries
* []() [OpenAI Gym](https://github.com/openai/gym)
* []() [Stable-Baselines 3](https://github.com/DLR-RM/stable-baselines3)
* []() [Tensorflow](https://www.tensorflow.org/)
* []() [Matplotlib](https://matplotlib.org/)

<p align="right">(<a href="#top">back to top</a>)</p>

## Installation

As of July 2022, because of current library incompatibilities, [python version 3.7](https://www.python.org/downloads/release/python-370/) needs to be installed.

1. Install the base Gym library with `pip install gym` 
2. Install stable-baselines with `pip install stable-baselines3` 
3. For compatibility reasons, an old version of tensorflow needs to be installed `pip install tensorflow==1.15.0` 
4. To display graphs in the main file, install matplotlib `pip install matplotlib` 

If problems occur, compare all library versions to the collection below:

<details>
  <summary>All Libraries/Versions used</summary>
  <ul>
    <li>absl-py              1.1.0</li>
    <li>ale-py               0.7.5</li>
    <li>argon2-cffi          21.3.0</li>
    <li>argon2-cffi-bindings 21.2.0</li>
    <li>astor                0.8.1</li>
    <li>attrs                21.4.0</li>
    <li>backcall             0.2.0</li>
    <li>beautifulsoup4       4.11.1</li>
    <li>bleach               5.0.1</li>
    <li>cffi                 1.15.1</li>
    <li>cloudpickle          2.1.0</li>
    <li>colorama             0.4.5</li>
    <li>cycler               0.11.0</li>
    <li>debugpy              1.6.0</li>
    <li>decorator            5.1.1</li>
    <li>defusedxml           0.7.1</li>
    <li>EditorConfig         0.12.3</li>
    <li>entrypoints          0.4</li>
    <li>fastjsonschema       2.15.3</li>
    <li>fonttools            4.33.3</li>
    <li>gast                 0.2.2</li>
    <li>google-pasta         0.2.0</li>
    <li>grpcio               1.47.0</li>
    <li>gym                  0.21.0</li>
    <li>gym-notices          0.0.7</li>
    <li>h5py                 3.7.0</li>
    <li>importlib-metadata   4.12.0</li>
    <li>importlib-resources  5.8.0</li>
    <li>ipykernel            6.15.0</li>
    <li>ipython              7.34.0</li>
    <li>ipython-genutils     0.2.0</li>
    <li>jedi                 0.18.1</li>
    <li>Jinja2               3.1.2</li>
    <li>joblib               1.1.0</li>
    <li>jsbeautifier         1.14.4</li>
    <li>jsonschema           4.6.1</li>
    <li>jupyter-client       7.3.4</li>
    <li>jupyter-core         4.10.0</li>
    <li>jupyterlab-pygments  0.2.2</li>
    <li>Keras-Applications   1.0.8</li>
    <li>Keras-Preprocessing  1.1.2</li>
    <li>kiwisolver           1.4.3</li>
    <li>lxml                 4.9.1</li>
    <li>Markdown             3.3.7</li>
    <li>MarkupSafe           2.1.1</li>
    <li>matplotlib           3.5.2</li>
    <li>matplotlib-inline    0.1.3</li>
    <li>mistune              0.8.4</li>
    <li>nbclient             0.6.6</li>
    <li>nbconvert            6.5.0</li>
    <li>nbformat             5.4.0</li>
    <li>nest-asyncio         1.5.5</li>
    <li>notebook             6.4.12</li>
    <li>numpy                1.21.6</li>
    <li>opencv-python        4.6.0.66</li>
    <li>opt-einsum           3.3.0</li>
    <li>packaging            21.3</li>
    <li>pandas               1.1.5</li>
    <li>pandocfilters        1.5.0</li>
    <li>parso                0.8.3</li>
    <li>pickleshare          0.7.5</li>
    <li>Pillow               9.1.1</li>
    <li>pip                  22.1.2</li>
    <li>prometheus-client    0.14.1</li>
    <li>prompt-toolkit       3.0.30</li>
    <li>protobuf             3.20.1</li>
    <li>psutil               5.9.1</li>
    <li>pycparser            2.21</li>
    <li>pygame               2.1.0</li>
    <li>Pygments             2.12.0</li>
    <li>pyparsing            3.0.9</li>
    <li>pyrsistent           0.18.1</li>
    <li>python-dateutil      2.8.2</li>
    <li>pytz                 2022.1</li>
    <li>pywin32              304</li>
    <li>pywinpty             2.0.5</li>
    <li>pyzmq                23.2.0</li>
    <li>scipy                1.7.3</li>
    <li>Send2Trash           1.8.0</li>
    <li>setuptools           57.0.0</li>
    <li>six                  1.16.0</li>
    <li>soupsieve            2.3.2.post1</li>
    <li>stable-baselines     2.10.2</li>
    <li>stable-baselines3    1.5.0</li>
    <li>tensorboard          1.15.0</li>
    <li>tensorflow           1.15.0</li>
    <li>tensorflow-estimator 1.15.1</li>
    <li>termcolor            1.1.0</li>
    <li>terminado            0.15.0</li>
    <li>tinycss2             1.1.1</li>
    <li>torch                1.12.0</li>
    <li>tornado              6.2</li>
    <li>traitlets            5.3.0</li>
    <li>typing_extensions    4.2.0</li>
    <li>wcwidth              0.2.5</li>
    <li>webencodings         0.5.1</li>
    <li>Werkzeug             2.1.2</li>
    <li>wheel                0.36.2</li>
    <li>wrapt                1.14.1</li>
    <li>zipp                 3.8.</li>
  </ul>
</details>

<p align="right">(<a href="#top">back to top</a>)</p>

## Usage

To create an environment, use the "Environment" class in rl_environment.py OR open the main.ipynb file and run all cells.

<p align="right">(<a href="#top">back to top</a>)</p>

## Project Organization

The repository contains multiple versions of the artifact. They are organized in folders beginning with the version number and ending with the newest implmented feature. Inside the version folder the structure is as follows:

    └── 0_example_feature               <- Version Folder
        │
        ├── main.ipynb                  <- Main notebook to train RL algorithmns and run simulations
        ├── rl_environment.py           <- RL environment
        │ 
        ├── simulation                  <- Folder: Simulation
        │   ├── simulation.py           <- Main simulation class. Controls actor classes. Starts simualtions
        │   │
        │   └── actor_classes           <- Folder: Contains all simulation actor classes
        │       ├── class_warehouse     <- Abstract Warehouse class and subclasses RegionalWarehouse and CentralWarehouse
        │       ├── class_customer      <- Customer class
        │       ├── class_manufacturer  <- Manufacturer class (Not available in all versions)
        │
        └── logfiles                    <- Folder: Contains created logfiles from main.ipynb (Not available in all versions)
            ├── logfile_date_time.json  <- Logfile containing information about a training/simulation run
            └── ...

<p align="right">(<a href="#top">back to top</a>)</p>
