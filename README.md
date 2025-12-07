# Machine Learning 4050U Final Project
----
## Steam Recommendation System

This project is made by Daniel Bryon, Beatriz Provido, and 
Gordon Law for our final project of machine learning 4050U. 
Compiling what we've learnt through the course and the research 
we have done to create a model which uses a graph neural network 
(GNN) to generate personalized game recommendations from a given 
input through link prediction. Utilizing libraries such as Pytorch,
Geometric, and Pandas to capture the patterns and deeper relationships 
between users and the games they play.

#### Features

* Graph Neural Network - Connecting users and steam games in a heterogeneous graph
* User Dataset - https://www.kaggle.com/datasets/kieranpoc/steam-reviews?select=weighted_score_above_08.csv
* Game Dataset - https://www.kaggle.com/datasets/nikatomashvili/steam-games-dataset

#### Tech Stack

* Frontend: Angular 19
* Backend: Flask 3.1.2
* Python 3.12.7
* Pytorch
* Pytorch Geometric

#### Project Structure

```
Steam Recommendation System
├── client
│   └── steam-recommender
│       │   public
│       │   └── assets
│       └── src
│           └── app
│               ├── components
│               │   ├── game-carousel
│               │   ├── game-highlight
│               │   ├── game-table
│               │   ├── header
│               │   ├── input
│               │   └── recommendation
│               └── services
├── server
│   ├── gnn
│   └── model
└── venv
```

## Prerequisites

1. Node.js v22.14.0
2. Npm v11.1.0
3. Angular CLI v19.2.0
4. Python v3.12.3

## Setup & Installation

1. Clone the repository github

2. Serving the backend:
    * Install python requirments
    ```
    # Within the root directory
    pip install -r requirements.txt
    ```
    * Move the model files into the server directory

    * Launch the flask server
    ```
    # Navigate into the server directory
    cd server

    # Starting the flask server
    python main.py
    ```

5. Serving the frontend:
    * Install the required angular packages
    ```
    # Within another ternimal, navigate into the angular frontend from the root directory
    cd client/webapp

    npm install
    ```

    * Launch the anular application
    ```
    npm start
    ```

#### Contributors 

* DCBryon
* BeatrizP02
* GordLaw

#### Resources

* https://github.com/Revadike/InternalSteamWebAPI
* https://docs.pytorch.org/docs/stable/index.html
* https://angular.dev/
* https://flask.palletsprojects.com/en/stable/
* https://uvadlc-notebooks.readthedocs.io/en/latest/index.html
* https://www.dgl.ai/dgl_docs/en/2.3.x/index.html