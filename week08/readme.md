# Project: Markov Simulation

### Team: Nora, Daniel, Wail, Matthias
# Repo: https://github.com/mfriebel/w8_Markov


## Goals
* **The project involves the following tasks:**

    1. explore the data (includes pandas wrangling)
    2. calculate transition probabilities (a 5x5 matrix)
    3. create a customer class and implement MCMC for one customer
    4. create a supermarket class that simulates multiple customers
    5. visualize the supermarket

* *Extra*:
    * fill the shelves of a supermarket image
    * clean up your code

This project may be complicated to complete on your own. Even in a team, you may want to focus on a few of the tasks at a time.

Please do the following:

Form a team of 2-4 people

Read the instructions carefully

Create a GitHub repository for the project

Invite all people on the team as collaborators

Discuss who does what


### 1. Explore Data (https://krspiced.pythonanywhere.com/chapters/project_markov/data_analysis.html#explore-supermarket-data)

Our sales department is interested in a summary of the collected data. Please generate a report including numbers and diagrams. Note that your audience are not data scientists, so take care to prepare insights that are as clear as possible. We are interested in the following:

* Calculate the total number of customers in each section   - *Wail*
* Calculate the total number of customers in each section over time     - *Nora*
* Display the number of customers at checkout over time     - *Nora*
* Calculate the time each customer spent in the market      - *Daniel*
* Calculate the total number of customers in the supermarket over time.     - *Daniel, Matthias*
* Our business managers think that the first section customers visit follows a different pattern than the following ones. Plot the distribution of customers of their first visited section versus following sections (treat all sections visited after the first as “following”).      - *Matthias*

#### Debugging Hints

* start by analyzing a single file
* each day, the customer IDs start again at 1. These are different customers anyway.
* when the shop closes, the remaining customers are rushed through the checkout. Their checkout is not recorded, so it may look as if they stay in the market forever.


### 2. Transition Probabilities (https://krspiced.pythonanywhere.com/chapters/project_markov/markov_chain/README.html#transition-probs)
-> Daniel
**Transition Probabilities**:
    * We would like to analyze how customers switch between sections of the supermarket. Calculate and visualize the probability of transitions from section A to B by counting all observed transitions.
    * E.g. if a customer was in the fruit section, later in the spices section, and went back to fruit, we observe two transitions: fruit → spices and spices → fruit .
    * The checkout is a special terminal state, from which customers cannot leave.
    * Draw a state diagram
    * Display the transition probability matrix
    * Visualize the probabilities as a heat map



**MC-Simulation**:
Use your transition probability matrix to propagate the states of an idealized population. Assume that there are infinite customers, so you can consider a state distribution.
The state distribution can be written as a vector of fractions:
`states = np.array([0.4, 0.6])  # e.g. cold, hot`

**Implement the following**:
    * Set an initial state distribution vector with all customers in the entrance
    * Store the state distribution in a result object (list, DataFrame or similar)
    * Calculate the next state as a dot product of your transition probability matrix P
    * Repeat from 2 for a number of steps
    * Plot the result

### 3. Monte-Carlo-Markov-Chain (https://krspiced.pythonanywhere.com/chapters/project_markov/classes/README.html#mcmc-simu)
->  Wail
### 4. Simulate a population (https://krspiced.pythonanywhere.com/chapters/project_markov/program_design/README.html#sim-population)
-> Nora
### 5. Visualise supermarket (https://krspiced.pythonanywhere.com/chapters/project_markov/classes/inheritance.html#draw-from-tiles)
-> Matthias
