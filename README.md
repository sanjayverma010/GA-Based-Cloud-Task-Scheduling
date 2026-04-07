# Cloud Task Scheduling using Genetic Algorithm (EA)

## Overview

This project implements Cloud Task Scheduling using an Evolutionary Algorithm (Genetic Algorithm) to optimize the allocation of tasks across Virtual Machines (VMs).

The goal is to minimize:

* Makespan (total execution time)
* Load imbalance
* Resource utilization cost

---

## Features

* Genetic Algorithm based optimization
* Task to VM allocation system
* Fitness evaluation (Makespan minimization)
* Modular Java architecture
* Scalable design
* Easy to extend with GUI

---

## How It Works

1. Initialize population (random task allocation)
2. Evaluate fitness (based on makespan)
3. Select best chromosomes
4. Apply crossover and mutation
5. Generate new population
6. Repeat until optimal solution is found

---

## Project Structure

```
CloudScheduler/
│
├── src/main/
│   ├── model/        # Task, VM, Chromosome
│   ├── algorithm/    # Genetic Algorithm logic
│   ├── service/      # Scheduler service
│   ├── utils/        # Fitness calculation
│   └── gui/          # GUI components (optional)
│
├── data/             # Sample input
└── README.md
```

---

## Technologies Used

* Java
* Object-Oriented Programming (OOP)
* Genetic Algorithm (Evolutionary Computing)

---

## Installation

1. Clone the repository:

```
git clone https://github.com/sanjayverma010/GA-Based-Cloud-Task-Scheduling.git
```

2. Navigate to the project directory:

```
cd GA-Based-Cloud-Task-Scheduling
```

3. Open the project in:

* IntelliJ IDEA
* Eclipse
* VS Code

---

## How to Run

1. Compile the project:

```
javac src/main/App.java
```

2. Run the program:

```
java src.main.App
```

Note: If using an IDE, simply run `App.java`.

---

## Example

```
Tasks: T1, T2, T3, T4
VMs: V1, V2, V3

Best Allocation:
[1, 2, 1, 3]

Makespan: 120
```

---

## Screenshots

Add your screenshots here after GUI implementation:

```
output.png
graph.png
```

Example:

* Task allocation view
* Makespan graph
* GUI interface

---

## Future Enhancements

* GUI using Java Swing or JavaFX
* Multi-objective optimization (time and cost)
* Real-time task simulation
* Comparison with FCFS and Round Robin

---

## Applications

* Cloud computing (AWS, Azure scheduling)
* Distributed systems
* Data centers
* Resource optimization problems

---

## Author

Sanjay Verma

---

## Contribution

Feel free to fork, improve, and contribute.
