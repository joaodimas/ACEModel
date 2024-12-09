# ACEModel

This repository contains the Python implementation of the agent-based model described in the master's thesis:

**Replication and Study of an Agent-Based Model of Industry Competition with R&D**  
Author: João Dimas
Pantheon-Sorbonne Master in Economics (2017)

### Overview

The implemented model is based on Chang (2015a), which describes an industry where heterogeneous firms compete by improving production efficiency through R&D. The primary objectives of the implementation are:

1. To replicate the results of Chang (2015a).
2. To experiment with two modifications to the original model:
   - The occurrence of abnormally large technological shocks.
   - The presence of multiple optimal technologies.

### Implementation Details

The model was coded from scratch in Python using object-oriented programming (OOP). This approach was chosen for the following reasons:

- **Code Readability**: Python offers a more accessible syntax compared to C++, facilitating understanding for economists without a computer science background.
- **Modular Design**: OOP separates the economic logic from technical implementation, improving the code's extensibility.
- **Independence**: The implementation does not rely on Chang's original code, ensuring a thorough understanding of the model's mechanisms.

### Features

- **Baseline Model**: Implements the Cournot competition framework with R&D, as described in Chang (2015a).
- **Extensions**:
  - Introduces periodic large shocks to the technological environment.
  - Simulates scenarios with multiple optimal technologies available simultaneously.
- **Simulation**: Produces dynamic results over 5,000 simulated periods for analysis.

### Requirements

- Python 3.x
- Standard libraries used include:
  - `numpy`
  - `matplotlib`
  - `random` (built-in)

### Usage

Clone the repository, install dependencies, and run the main script. Modify configuration files to explore custom scenarios or provided extensions.

### Outputs

The simulation generates time-series data and visualizations, including:
- Number of firms in the market
- Industry output and profits
- Technological proximity and marginal costs

---

For further details, refer to the thesis document or contact the author.
