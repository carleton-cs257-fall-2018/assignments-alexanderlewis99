Alec Wang and Bat-Orgil Batjargal

Brief description:
For our project, we will create a cellular automaton that simulates the growth of tumor cells. Our tumor population is made of up two types of cell: cancer stem cells and non-stem cancer cells. At each simulation timestep, these cells can proliferate, can migrate into vacant adjacent spaces, and can undergo spontaneous death. How and when they do these three things depend on their instance variables, which can differ between the stem and non-stem cells. While they both have the same probability of dividing and migrating, non-stem cells can divide only ten times before dying and produce only more non-stem cells, while stem cells can divide infinitely many times and have a 10% chance of producing another stem cell. The daughter cells appear in spaces adjacent to the parent cell that are free in the grid.
Our project idea is inspired by the article: Poleszczuk J., Enderling H. A high-performance cellular automaton model of tumor growth with dynamically growing domains. Applied Mathematics. 2014.

A brief argument of why MVC is appropriate:
An MVC pattern is appropriate for our project because each cell in the simulation will have its own data and that data will change as it is constantly updated. When updated, the controller registers that change and updates the pixel counterpart of the cell in the View. Our Models include be different types of cells, each with a different behavior: cancer stem cells, non-stem cancer cells, dead cells, and  empty cells (unoccupied squares). We also have a model called a Lattice that keeps track of all the cells and communicates with the Controller as the cells in the lattice divide, migrate, and die. The Controller will updates the view as it receives information about changes to the data from the lattice changes. The View receives inputs from user about changes to the settings of the simulation and communicates that data to the Controller, which then passes it along to the Lattice Model. To simulate cancer cell life using cellular automatom, MVC is a great design choice.

Core classes that make up our model:
Cell.java - the parent class for all the other cells
EmptyCell.java - used to represent empty squares in the lattice. It's represented by white pixels in the view.
DeadCell.java - the class for dead cells which are represented by a black pixel in the view.
AliveCell.java - the parent class for alive cells (stem cells and non-stem cells).
StemCell.java - the initial cells that give rise to non-stem cells. They're represented by blue pixels in the view.
NonStemCell.java - the class for the majority of cells. They are daughters of stem cells and die after dividing many times. They are represented by blue pixels in the view.
Lattice.java - contains all of the cells in the simulation and keeps track of the changes they undergo as well as their pixel counterparts.

Brief status about the current state of the program: 11/19/18
Everything appears to work as there are no bugs or crashes occurring. I made adjustments to the names of the sliders to improve clarity as you recommended to me Jeff. I hope you have a good winter break! :)