/**
 * Lattice.java
 * Alec Wang and Bat-Orgil Batjargal, 11/19/18.
 *
 * A java class for a two-dimensional square lattice of cells. It has the ability to update them over time.
 */

package tumorSimulation;
import javafx.fxml.FXML;
import javafx.scene.control.Slider;

import java.awt.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;
import java.awt.image.BufferedImage;

public class Lattice extends BufferedImage{

    private ArrayList<ArrayList> cellLattice= new ArrayList<>();
    private ArrayList<Point> cellWatchlist = new ArrayList<>();
    private ArrayList<Point> cells_to_add_to_watchlist = new ArrayList<>();
    private ArrayList<Point> cells_to_remove_from_watchlist = new ArrayList<>();
    private int numRows;
    private int numColumns;
    private int timestep;
    private int generalCct;
    private int nonStemMaxProliferation;
    private int generalMotilitySpeed;
    private double nonStemProbabilityOfDying;
    private double stemProbabilityOfDaughter;
    private boolean traitVectorJustUpdated;

    /**
     * Constructor for a lattice of cells
     * @param height - number of rows in the lattice
     * @param width - number of columns in the lattice
     * @param imageType - type of bufferedImage for the lattice
     */
    public Lattice(int height, int width, int imageType){
        super(width, height, imageType);
        this.numRows = height;
        this.numColumns = width;
        this.generalCct = 24;
        this.nonStemMaxProliferation = 10;
        this.generalMotilitySpeed = 5;
        this.nonStemProbabilityOfDying = 0.01;
        this.stemProbabilityOfDaughter = 0.1;
        this.traitVectorJustUpdated = false;
        this.timestep = 0;
        this.constructLattice();
    }

    /**
     * Constructs the two dimensional ArrayList so that it contains all the cells in the lattice
     */
    public void constructLattice(){
        for (int i = 0; i < this.numRows; i++){
            ArrayList<Cell> lattice_row = new ArrayList<Cell>();
            for (int j = 0; j < this.numColumns; j++){
                lattice_row.add(new EmptyCell());
            }
            this.cellLattice.add(lattice_row);
        }
        Random rand = new Random();
        int y_random = rand.nextInt(this.numRows-1);
        int x_random = rand.nextInt(this.numColumns-1);
        Point first_stem_cell_coords = new Point(x_random, y_random);
        Cell first_stem_cell = new StemCell();
        this.setCell(first_stem_cell_coords, first_stem_cell);
        this.cellWatchlist.add(first_stem_cell_coords);
    }

    /**
     * Get the number of rows in the lattice
     * @return number of rows
     */
    public int getNumRows(){
        return this.numRows;
    }

    /**
     * Get the number of columns in the lattice
     * @return number of columns
     */
    public int getNumCols(){
        return this.numColumns;
    }

    /**
     * Get a row of cells of the lattice
     * @param row_index - the index of the row which you wish to get
     * @return an arraylist of cells in the lattice
     */
    private ArrayList<Cell> getRow(int row_index){
        return this.cellLattice.get(row_index);
    }

    /**
     * Set a row of the lattice as a row of cells
     * @param row_index - the index of the row which you wish to replace
     * @param new_row - a list of cells to be the new row
     * @throws IllegalArgumentException
     */
    public void setRow(int row_index, ArrayList<Cell> new_row){
        cellLattice.set(row_index, new_row);
        if (new_row.size() != this.numColumns) {
            throw new IllegalArgumentException();
        }
    }

    /**
     * Get a cell from the lattice
     * @param cell_coordinates - the coordinates of the cell to get
     * @return the cell from the lattice
     */
    public Cell getCell(Point cell_coordinates){
        int x = (int) cell_coordinates.getX();
        int y = (int) cell_coordinates.getY();
        ArrayList<Cell> lattice_row = this.cellLattice.get(y);
        Cell cell = lattice_row.get(x);
        return cell;
    }

    /**
     * Replace a cell in the lattice with a new cell
     * @param cell_coordinates - the coordinates of the cell to replace
     * @param new_cell - the new cell that will replace the old cell
     */
    public void setCell(Point cell_coordinates, Cell new_cell){
        int x = (int) cell_coordinates.getX();
        int y = (int) cell_coordinates.getY();
        ArrayList<Cell> lattice_row = this.cellLattice.get(y);
        lattice_row.set(x, new_cell);
        this.cellLattice.set(y, lattice_row);
    }

    /** Gets a stem or non-stem cell as an AliveCell object from the CellLattice
     * @param cell_coordinates - the coordinates of the living cell
     * @return a living cell
     */
    public AliveCell getLivingCell(Point cell_coordinates){
        String cell_type = this.getCell(cell_coordinates).getCellType();
        AliveCell cell;
        if (cell_type == "non-stem"){
            cell = (NonStemCell) this.getCell(cell_coordinates);
        } else {
            cell = (StemCell) this.getCell(cell_coordinates);
        }
        return cell;
    }

    /**
     * Iterates through the cellArray, receives the behavior of each cell, and acts upon it.
     */
    public void updateCells(){
        this.timestep++;
        for (Point cell_coords: this.cellWatchlist) {
            AliveCell cell = getLivingCell(cell_coords);
            Map<String, Boolean> behavior = cell.getBehaviorForTimestep();
            this.updateCellBasedOnBehavior(cell, cell_coords, behavior);
        }
        this.cellWatchlist.addAll(cells_to_add_to_watchlist);
        this.cellWatchlist.removeAll(cells_to_remove_from_watchlist);
        this.cells_to_add_to_watchlist.clear();
        this.cells_to_remove_from_watchlist.clear();
        if(this.traitVectorJustUpdated){
            this.updateTraitVectorsOfCellsInWatchList();
            this.traitVectorJustUpdated = false;
        }
    }

    /**
     * Updates the cell and the cellLattice based on the cell's behavior
     * @param cell - the cell to update
     * @param cell_coords - the coordinates of the cell
     * @param behavior - the dictionary detailing whether the cell dies, divides, and/or migrates
     */
    private void updateCellBasedOnBehavior(AliveCell cell, Point cell_coords, Map<String, Boolean> behavior){
        if(behavior.get("die")){
            this.kill_cell(cell_coords);
        }
        else {
            //migrate and divide are time-step independent
            if(this.getEmptyAdjacentSpot(cell_coords)!=null){
                if(behavior.get("divide")){
                    this.divide_cell(cell_coords, cell);
                }
                if(behavior.get("migrate")){
                    Point new_cell_coords = this.getEmptyAdjacentSpot(cell_coords);
                    //need to check twice because divide may fill the only available spot
                    if (new_cell_coords != null){
                        this.move_cell(cell_coords, new_cell_coords, cell);
                    }
                }
            } //imperfect logic but runs much faster
            else {
                this.cells_to_remove_from_watchlist.add(cell_coords);
            }
        }
    }

    /**
     * Divides a cell by creating a daughter a cell
     * @param parent_cell_coords the coordinates of the cell that is dividing
     * @param parent - the cell that is dividing
     */
    private void divide_cell(Point parent_cell_coords, AliveCell parent){
        Point daughter_cell_coordinates = getEmptyAdjacentSpot(parent_cell_coords);
        //unnecessary check because of where the method is called but keep just in case
//        if (daughter_cell_coordinates != null){
            String daughter_cell_type = parent.getCellTypeOfNewDaughter();
            AliveCell daughter_cell = this.getNewDaughterCell(daughter_cell_type);
            this.setCell(daughter_cell_coordinates, daughter_cell);
            this.updateCellColorInLattice(daughter_cell_coordinates, daughter_cell_type);
            this.cells_to_add_to_watchlist.add(daughter_cell_coordinates);
            this.checkMaxProliferationAfterDivision(parent, parent_cell_coords);
//        }
    }

    /**
     * Gets a new StemCell or NonStemCell
     * @param daughter_cell_type - the cell type of the daughter
     * @return a StemCell or NonStemCell depending on the daughter cell-type
     */
    private AliveCell getNewDaughterCell(String daughter_cell_type){
        AliveCell daughter_cell;
        if(daughter_cell_type == "non-stem"){
            daughter_cell = new NonStemCell(this.generalCct, this.nonStemMaxProliferation , this.generalMotilitySpeed, this.nonStemProbabilityOfDying);
        } else {
            daughter_cell = new StemCell(this.generalCct, this.generalMotilitySpeed, this.stemProbabilityOfDaughter);
        }
        return daughter_cell;
    }

    /**
     * Set the cell's cell-type to dead and updates its pixel counterpart in the bufferedImage
     * @param cell_coords - the coordinates of the cell to kill
     */
    private void kill_cell(Point cell_coords){
        this.setCell(cell_coords, new DeadCell());
        this.updateCellColorInLattice(cell_coords, "dead");
        this.cells_to_remove_from_watchlist.add(cell_coords);
    }

    /**
     * Checks the MaxProliferation of the cell and, if it is a non-stem cell, kills it if it hits 0
     * @param parent - the parent cell
     * @param parent_coordinates - the coordinates of the parent cell
     */
    private void checkMaxProliferationAfterDivision(AliveCell parent, Point parent_coordinates){
        if (parent.getCellType() == "non-stem") {
            int current_max_proliferation = parent.getMaxProliferation();
            if (current_max_proliferation == 1) {
                this.kill_cell(parent_coordinates);
            } else {
                parent.setMaxProliferation(current_max_proliferation - 1);

            }
        }
    }

    /**
     * Moves a cell from one point to another point in the lattice and updates the pixel counterparts in the bufferedImage
     * @param cell_coords - the current coordinates of the cell to move
     * @param new_cell_coords - the new coordinates for the cell
     * @param cell_to_move - the cell to move
     */
    private void move_cell(Point cell_coords, Point new_cell_coords, Cell cell_to_move){
        this.setCell(cell_coords, new EmptyCell());
        this.updateCellColorInLattice(cell_coords, "empty");
        this.setCell(new_cell_coords, cell_to_move);
        this.updateCellColorInLattice(new_cell_coords, cell_to_move.getCellType());
        this.cells_to_add_to_watchlist.add(new_cell_coords);
        this.cells_to_remove_from_watchlist.add(cell_coords);
    }

    /** Changes the trait vectors for new cells
     * @param newGeneralCct - the new cell cycle time for all cells
     * @param newGeneralMotilitySpeed - the new motility speed for all cells
     * @param newStemProbabilityOfDaughterIsStem - the new probability for stem cells that their daughter cell is a stem cell
     * @param newNonStemMaxProliferation - the new max proliferation limit for non stem cells
     * @param newNonStemProbabilityOfDying - the new probability of dying for non stem cells
     */
    public void updateTraitVector(int newGeneralCct, int newGeneralMotilitySpeed, double newStemProbabilityOfDaughterIsStem, int newNonStemMaxProliferation,  double newNonStemProbabilityOfDying){
        if (this.generalCct != newGeneralCct){
            this.generalCct = newGeneralCct;
            this.traitVectorJustUpdated = true;
        }
        if (this.generalMotilitySpeed != newGeneralMotilitySpeed){
            this.generalMotilitySpeed = newGeneralMotilitySpeed;
            this.traitVectorJustUpdated = true;
        }
        if (this.stemProbabilityOfDaughter != newStemProbabilityOfDaughterIsStem){
            this.stemProbabilityOfDaughter = newStemProbabilityOfDaughterIsStem;
            this.traitVectorJustUpdated = true;
        }
        if (this.nonStemMaxProliferation != newNonStemMaxProliferation){
            this.nonStemMaxProliferation = newNonStemMaxProliferation;
            this.traitVectorJustUpdated = true;
        }
        if (this.nonStemProbabilityOfDying != newNonStemProbabilityOfDying){
            this.nonStemProbabilityOfDying = newNonStemProbabilityOfDying;
            this.traitVectorJustUpdated = true;
        }
    }

    /**
     * Updates the trait vector of currently actively cells in the cellWatchList
     */
    private void updateTraitVectorsOfCellsInWatchList(){
        for (Point cell_coordinates: this.cellWatchlist) {
            AliveCell cell = this.getLivingCell(cell_coordinates);
            cell.setCct(this.generalCct);
            cell.setMotilitySpeed(this.generalMotilitySpeed);
            if(cell.getCellType() == "stem"){
                cell.setProbabilityOfDaughterStemCell(this.stemProbabilityOfDaughter );

            } else {
                cell.setMaxProliferation(this.nonStemMaxProliferation );
                cell.setProbabilityOfDying(this.nonStemProbabilityOfDying);
            }
            cell.updateProbabilityOfDividing();
            cell.updateProbabilityOfMigrating();
        }
    }

    /**
     * @return boolean - whether the lattice is full or not
     */
    public boolean isDone(){
        return (this.cellWatchlist.size()==0);
    }
    /**
     * Changes the color of a point in the bufferedImage
     * @param cell_coords - the coordinates of the cell
     * @param cell_type - the type of cell
     */
    private void updateCellColorInLattice(Point cell_coords, String cell_type){
        int x = (int) cell_coords.getX();
        int y = (int) cell_coords.getY();
        int rgb  = 0;
        if (cell_type.equals("empty")) {
            rgb = new Color(255, 255, 255).getRGB(); //white
        }
        if (cell_type.equals("non-stem")){
            rgb = new Color(255, 0, 0).getRGB();; //red
        } else if (cell_type.equals("stem")){
            rgb = new Color(40, 82, 0).getRGB();; //yellow
        } else if (cell_type.equals("dead")){
            rgb = new Color(2, 2, 2).getRGB(); //black
        }
        this.setRGB(x, y, rgb);
    }

    /**
     * Finds an empty adjacent square in the lattice to a cell if one exists
     * @param cell_coords - the coordinates of the cell
     * @return the coordinates of the empty adjacent square
     */
    private Point getEmptyAdjacentSpot(Point cell_coords){
        ArrayList<Point> avaliableCoords = getAvailableCoordinates(cell_coords);
        if (avaliableCoords.size() == 0){
            return null;
        }
        return getRandomPointUsingMonteCarloSampling(avaliableCoords);
    }

    /**
     * Gets a random point from a set of points using Monte Carlo sampling
     * @param coordinates - an arraylist of points to sample from
     * @return a random coordinate
     */
    private Point getRandomPointUsingMonteCarloSampling(ArrayList<Point> coordinates){
        int numChoices = coordinates.size();
        Random rand = new Random();
        double chance = rand.nextDouble(); // generates between 0 and 1
        double higher_end = 1;
        double lower_end = 1 - (double) 1/numChoices;
        for (int chosenOption = numChoices - 1; chosenOption >= 0; chosenOption = chosenOption - 1){
            if (chance < higher_end && chance > lower_end){
                return coordinates.get(chosenOption);
            } else {
                higher_end = higher_end - (double) 1/numChoices;
                lower_end = lower_end - (double) 1/numChoices;
            }
        }
        return coordinates.get(0); //unnecessary because when lower_end reaches 0, the if statement in the for loop will be true
    }


    /**
     * Gets coordinates of available (empty/dead) adjacent squares to a given cell
     * @param cell_coordinates the coordinates of the cell to find available squares adjacent to
     * @return coordinates of available adjacent squares
     */
    private ArrayList<Point> getAvailableCoordinates(Point cell_coordinates){
        ArrayList<Point> all_eight_neighbors = this.getPotentialNeighborsCoords(cell_coordinates);
        ArrayList<Point> neighbors = this.removeNeighborsOutOfBounds(all_eight_neighbors);
        ArrayList<Point> available_squares = this.removeLivingNeighbors(neighbors);
        return available_squares;
    }

    /**
     * Removes coordinates of stem or non-stem cell
     * @param neighbors - ArrayList of neighbor coordinates in bounds of lattice
     * @return neighbors - an ArrayList of coordinates of empty/dead neighbors
     */
    private ArrayList<Point> removeLivingNeighbors(ArrayList<Point> neighbors){
        ArrayList<Point> neighbors_to_remove = new ArrayList<>();
        for (Point neighbor_coordinate: neighbors){
            Cell cell = this.getCell(neighbor_coordinate);
            if (cell.getCellType().equals("stem") || cell.getCellType().equals("non-stem")){
                neighbors_to_remove.add(neighbor_coordinate);
            }
        }
        for (Point living_neighbor: neighbors_to_remove){
            neighbors.remove(living_neighbor);
        }
        return neighbors;
    }

    /**
     * Removes generated impossible coordinates
     * @param neighbors - an ArrayList of Points
     * @return an ArrayList of Points
     */
    private ArrayList<Point> removeNeighborsOutOfBounds(ArrayList<Point> neighbors){
        ArrayList<Point> neighbors_to_remove = new ArrayList<>();
        for (Point coordinate: neighbors) {
            int x = (int) coordinate.getX();
            int y = (int) coordinate.getY();
            if (x < 0 || x >= this.numColumns || y < 0 || y >= this.numRows){
                neighbors_to_remove.add(coordinate);
            }
        }
        for (Point neighbor_out_of_bounds: neighbors_to_remove){
            neighbors.remove(neighbor_out_of_bounds);
        }
        return neighbors;
    }

    /**
     * Generate possible 8 neighbors coordinates
     * @param cell_coords - coordinates of the dividing/migrating cell
     * @return an ArrayList of all adjacent, including ones outside the bounds of the lattice
     */
    private ArrayList<Point> getPotentialNeighborsCoords(Point cell_coords){
        int x = (int) cell_coords.getX();
        int y = (int) cell_coords.getY();
        ArrayList<Point> all_eight_neighbors = new ArrayList<>();
        for (int i = -1; i <= 1; i++){
            for (int j = -1; j <= 1; j++){
                if (!(i == 0 && j == 0)){
                    Point point = new Point(x + i, y + j);
                    all_eight_neighbors.add(point);
                }
            }
        }
        return all_eight_neighbors;
    }
}