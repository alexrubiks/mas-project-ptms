# Project Report: Public Transport Mobility Simulation

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

## Next Steps: Introducing Disruptions
To enrich the simulation, disruptions can be introduced into the system in the menu:
1. **Road Closures:** Simulating blocked roads to observe how pedestrians and buses route.
2. **Bus Breakdowns:** Modeling missing buses to measure the resulting delays.

These disruptions aim to observe how agents adapt to unexpected changes and quantify the impact on passenger travel times.

## Conclusion
The project has successfully established a base model for simulating urban mobility, incorporating the behavior of pedestrians and buses. The next steps involve disruptions to evaluate system resilience and adaptability.

### Results Examples

| Without Bus | 3 Bus Lines (B, C, D) | All Bus Lines |
|-------------|------------------------|---------------|
| ![Without bus](https://github.com/user-attachments/assets/bf9bafe4-f2aa-4dfe-89b0-2fd7aa767a9c) | ![3 bus lines](https://github.com/user-attachments/assets/94d774e7-72ed-4f28-92e5-f6fe23f810d9) | ![All bus lines](https://github.com/user-attachments/assets/11a60cda-4c16-4c46-ac77-a88d8c4d7121) |



