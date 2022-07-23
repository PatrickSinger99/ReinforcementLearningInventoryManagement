<div id="top"></div>

# ReinforcementLearningInventoryManagement


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#project-organization">Project Organization</a></li>
  </ol>
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

<p align="right">(<a href="#top">back to top</a>)</p>

## Usage

To create an environment, use the "Environment" class in rl_environment.py OR open the main.ipynb file and run all cells.

<p align="right">(<a href="#top">back to top</a>)</p>

## Project Organization

<p align="right">(<a href="#top">back to top</a>)</p>
