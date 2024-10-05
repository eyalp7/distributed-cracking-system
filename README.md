# MD5 Cracking Distributed System

## Overview

This project implements a distributed computing system in Python to find the 10-digit string that generates the MD5 hash `1813301B31853F1B98A18EDCC7F0C9EC`. The system is structured in a client-server architecture, where a single server distributes tasks among multiple clients, optimizing the computation across available resources.

## Features

- **Client-Server Architecture**: A single server distributes work to multiple clients.
- **Dynamic Task Allocation**: The server manages which combinations have been tried and assigns number blocks to clients based on their processing capabilities.
- **Resource Optimization**: Clients adjust their workload according to the number of CPU cores available, ensuring maximum utilization of system resources.
- **Threading Support**: Utilizes Python’s `threading` module to efficiently manage multiple computations within each client.

## Requirements

- Python 3.x
- Basic knowledge of networking and Python programming
- `threading` module (included in standard Python distribution)

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/md5.git
   cd md5

2. **Run the server and clients**:
  ```bash
  python server.py
  python client.py
