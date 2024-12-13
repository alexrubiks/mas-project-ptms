Project Report: Public Transport Mobility Simulation
------------------------------------------------------
TREMELLAT Alexis & PERRIOT Mathieu - 2024
___
## Introduction
This project focuses on designing and implementing a multi-agent system to simulate the movement of passengers and public transport vehicles within a city. The city is represented by roads and bus stops. Passengers have defined origins and destinations, which they can reach by walking or using public transport (buses). Buses follow predefined schedules. The main goal is to simulate these interactions and measure the impact of disruptions on passengers' travel times.

## Current state

### City Representation
- The city is modeled as a grid where intersections represent bus stops, and roads connect these points.
- Specific points in the grid are randomly designated as origins and destinations on walking area for passengers.

### Pedestrian Behavior
- Pedestrians are agents.
- Pedestrians are programmed to choose the fastest route to their destination, either by walking and using buses.

### Bus Representation
- Buses are modeled as agents with predefined routes and fixed schedules.
- Each bus can take waiting passengers.
- Bus stops are key interaction points where passengers board and alight.

### Interactions Between Agents
- Pedestrians calculate travel times for both walking and bus options.
- Buses adhere to schedules and interact with passengers at stops.

## Results Achieved
- A functional simulation where pedestrians and buses move consistently within the city.
- Pedestrians dynamically switch between walking and buses to minimize travel time.

## Introducing Disruptions
To enrich the simulation, disruptions can be introduced into the system in the menu:
1. **Road Closures:** Simulating blocked roads to observe how pedestrians and buses route.
2. **Bus Breakdowns:** Modeling missing buses to measure the resulting delays.

These disruptions aim to observe how agents adapt to unexpected changes and quantify the impact on passenger travel times.

## Difficulties Encountered

### Pedestrian Behavior
- Implementing the logic for pedestrians to choose between walking and bus travel.
- Calculating their travel was challenging because first implementation was not efficient (took way longer than expected and slow down the simulation).

### Bus Representation
- Ensuring buses follow their routes and schedules correctly.
- Managing the interactions between buses and passengers at stops.


## How to use the simulation

### Requirements
- Python 3.13 or higher.
- Pygame library.

### Running the simulation
1. Clone the repository.
2. Install the required libraries.
3. Run the `__main__.py` file.
4. Use the menu to introduce disruptions and observe the agents' behavior.
5. Start the simulation.

### Menu Options
The menu allows you to:
- Start the simulation. 
- Introduce road closures (click on the road to close it) 
- Increase or decrease the number of bus.
- Remove bus lines. (A, B, C, D)
- Place park instead of building. (click on the building to change it)

### Simulation Display
Once the simulation starts, you can se pedestrians moving around the city, buses following their routes, and passengers boarding and alighting at bus stops.
You also have a on the right side of the screen a quick overview of the simulation state.

To change the options you may need to stop the simulation, change it through the menu and start the simulation again.

## Conclusion
This project has successfully developed a robust simulation framework for urban mobility, incorporating dynamic pedestrian and bus behaviors within a city grid. The system enables passengers to adaptively choose between walking and bus travel to minimize their travel time, with realistic interactions such as boarding and alighting at bus stops. Additionally, the simulation allows for disruptions like road closures and bus breakdowns, offering a valuable tool to study urban transport resilience.

The quick dashboard allows users to monitor the simulation state, allowing them to observe the impact of disruptions on passenger travel times and system performance.

### Results Examples

| Without Bus | 3 Bus Lines (B, C, D) | All Bus Lines |
|-------------|------------------------|---------------|
| ![Without bus](https://github.com/user-attachments/assets/bf9bafe4-f2aa-4dfe-89b0-2fd7aa767a9c) | ![3 bus lines](https://github.com/user-attachments/assets/94d774e7-72ed-4f28-92e5-f6fe23f810d9) | ![All bus lines](https://github.com/user-attachments/assets/11a60cda-4c16-4c46-ac77-a88d8c4d7121) |



