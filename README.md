# Route Planning

## ✨ Project Description ✨
In this project, I implemented a **Uniform Cost Search Algorithm** that can find the shortest route between any two cities.

Run Command: `python find_route.py input_file_name.txt origin_city destination_city`
  - Example: `python find_route.py spain.txt Burgos Segovia`

I used a tree search framework, meaning that the algorithm uses a single queue (frontier) and does not keep track of which cities have been explored. I used a tree search instead of a graph search framework so that I could simulate a real-world environment where memory is limited and having multiple memory queues is not a viable option.


## ✔ Contents of Repository
- The program is called find_route.py and it takes in an input file such as spain.txt
  - Note: spain.txt is an example file that I created. Anyone can create a new file for another country or set of countries and use that instead. Another example file in this repository is germany_england.txt
- spain.txt describes the road system in Spain which can be visualized in the figure below. Each line in spain.txt represents the road connecting two cities.
  - For example, the line ***Burgos Segovia 197*** indicates that there exists a road that is 197 km long and connects the cities Burgos and Segovia.
- tests_spain.txt contains some examples that can be used to test the functionality of the code. tests_germany_london.txt is the equivalent test file for the Germany/England map

![image](https://user-images.githubusercontent.com/70923397/169309232-22188559-1777-49c3-bb55-7ea3089a81ee.png)


## 🧐 Program Output
There are three different possible outputs (refer to Spain figure above):

- There exists at least one route between the two input cities
  - Command: `python find_route.py spain.txt Lugo Valencia`
  - Output: 
  ```
  distance: 1010 km
  route:
  Lugo to Leon, 236 km
  Leon to Valladolid, 134 km
  Valladolid to Segovia, 111 km
  Segovia to Madrid, 87 km
  Madrid to Albacete, 251 km
  Albacete to Valencia, 191 km
  ```
- The two input cities are the same
  - Command: `python find_route.py spain.txt Burgos Burgos`
  - Output: 
  ```
  distance: 0 km
  route:
  Burgos to Burgos, 0 km
  ```
- No route exists between the two input cities
  - Command: `python find_route.py spain.txt Madrid Tenerife`
  - Output: 
  ```
  distance: infinity
  route:
  none
  ```
