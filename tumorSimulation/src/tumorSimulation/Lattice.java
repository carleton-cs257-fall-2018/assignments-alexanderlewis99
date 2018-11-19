/**
 * Lattice.java
 * Alec Wang and Bat-Orgil Batjargal, 11/19/18.
 *
 * A java class for a two-dimensional square lattice of cells. It has the ability to update them over time.
 */

package tumorSimulation;
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
    private ArrayList<Point> surrounded_living_cells = new ArrayList<>();
    private int numRows;
    private int numColumns;
    private int generalCct;
    private int nonStemMaxProliferation;
    private int generalMotilitySpeed;
    private double nonStemProbabilityOfDying;
    private double stemProbabilityOfDaughter;
    private boolean cellTraitsJustUpdated;

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
        this.cellTraitsJustUpdated = false;
        this.constructLattice();
    }

    /**
     * Constructs the two dimensional ArrayList so that it contains all the cells in the lattice
     */
    public void constructLattice(){
        for (int r = 0; r < this.numRows; r++){
            ArrayList<Cell> lattice_row = new ArrayList<Cell>();
            for (int c = 0; c < this.numColumns; c++){
                lattice_row.add(new EmptyCell());
            }
            this.cellLattice.add(lattice_row);
        }
        Random rand = new Random();
        int random_y = rand.nextInt(this.numRows-1);
        int random_x = rand.nextInt(this.numColumns-1);
        Point first_stem_cell_coords = new Point(random_x, random_y);
        this.setCell(first_stem_cell_coords, new StemCell());
        this.cellWatchlist.add(first_stem_cell_coords);
    }


    public int getNumRows(){
        return this.numRows;
    }


    public int getNumCols(){
        return this.numColumns;
    }

    public Cell getCell(Point cell_coordinates){
        int x = (int) cell_coordinates.getX();
        int y = (int) cell_coordinates.getY();
        ArrayList<Cell> lattice_row = this.cellLattice.get(y);
        Cell cell = lattice_row.get(x);
        return cell;
    }

    public void setCell(Point coordinates, Cell new_cell){
        int x = (int) coordinates.getX();
        int y = (int) coordinates.getY();
        ArrayList<Cell> lattice_row = this.cellLattice.get(y);
        lattice_row.set(x, new_cell);
        this.cellLattice.set(y, lattice_row);
    }

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

    public void addStemCellFromClick(Point click_coordinates){
        this.setCell(click_coordinates, new StemCell());
        this.cellWatchlist.add(click_coordinates);
    }

    public boolean isDone(){
        return (this.cellWatchlist.size()==0);
    }

    /**
     * Updates the cells and the cellWatchList, which keeps track of which cells need to be updated
     */
    public void updateSimulation(){
        this.updateCells();
        this.cellWatchlist.addAll(cells_to_add_to_watchlist);
        this.cellWatchlist.removeAll(cells_to_remove_from_watchlist);
        this.cells_to_add_to_watchlist.clear();
        this.cells_to_remove_from_watchlist.clear();
        if(this.cellTraitsJustUpdated){
            this.updateTraitVectorsOfCellsInWatchList();
            this.cellTraitsJustUpdated = false;
        }
        if(this.cellWatchlist.size()==0){
            this.addUnsurroundedAliveCellsIfExistToWatchList();
        }
    }

    /**
     * Iterates through the cellArray, receives the behavior of each cell, and acts upon it.
     */
    public void updateCells(){
        for (Point cell_coords: this.cellWatchlist) {
            String cell_type = getCell(cell_coords).getCellType();
            if(cell_type == "dead" || cell_type == "empty"){
                this.cells_to_remove_from_watchlist.add(cell_coords);
            } else {
                AliveCell cell = getLivingCell(cell_coords);
                Map<String, Boolean> behavior = cell.getBehaviorForTimestep();
                this.updateCellBasedOnBehavior(cell, cell_coords, behavior);
            }
        }
    }

    /**
     * Updates the cell and its affect on cellLattice based on the cell's behavior
     * @param cell - the cell to update
     * @param cell_coords - the coordinates of the cell
     * @param behavior - the dictionary detailing whether the cell dies, divides, and/or migrates
     */
    private void updateCellBasedOnBehavior(AliveCell cell, Point cell_coords, Map<String, Boolean> behavior){
        if(behavior.get("die")){
            this.kill_cell(cell_coords);
        }
        else {
            if(this.hasEmptyAdjacentSpot(cell_coords)){
                if(behavior.get("divide")){
                    this.divide_cell(cell_coords, cell);
                }
                if(behavior.get("migrate")){
                    //need to check hasEmptyAdjacentSpot() twice
                    // because divide may fill the only available spot
                    if (this.hasEmptyAdjacentSpot(cell_coords)){
                        this.migrate_cell(cell_coords, cell);
                    }
                    else {
                        this.cells_to_remove_from_watchlist.add(cell_coords);
                        this.surrounded_living_cells.add(cell_coords);
                    }
                }
            }
            else {
                this.cells_to_remove_from_watchlist.add(cell_coords);
                this.surrounded_living_cells.add(cell_coords);
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
        String daughter_cell_type = parent.getCellTypeOfNewDaughter();
        AliveCell daughter_cell = this.getNewDaughterCell(daughter_cell_type);
        this.setCell(daughter_cell_coordinates, daughter_cell);
        this.updateCellColorInLattice(daughter_cell_coordinates, daughter_cell_type);
        this.cells_to_add_to_watchlist.add(daughter_cell_coordinates);
        this.checkMaxProliferation(parent, parent_cell_coords);
    }

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
    private void checkMaxProliferation(AliveCell parent, Point parent_coordinates){
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
     * @param cell_coords - the current coordinates of the cell to move
     * @param cell_to_move - the cell to move
     */
    private void migrate_cell(Point cell_coords, Cell cell_to_move){
        Point new_cell_coords = this.getEmptyAdjacentSpot(cell_coords);
        this.setCell(cell_coords, new EmptyCell());
        this.updateCellColorInLattice(cell_coords, "empty");
        this.setCell(new_cell_coords, cell_to_move);
        this.updateCellColorInLattice(new_cell_coords, cell_to_move.getCellType());
        this.cells_to_add_to_watchlist.add(new_cell_coords);
        this.cells_to_remove_from_watchlist.add(cell_coords);
    }

    /** Changes the trait vectors–the characteristics–for new cells
     * @param newGeneralCct - the new cell cycle time for all cells
     * @param newGeneralMotilitySpeed - the new motility speed for all cells
     * @param newStemProbabilityOfDaughterIsStem - the new probability for stem cells that their daughter cell is a stem cell
     * @param newNonStemMaxProliferation - the new max proliferation limit for non stem cells
     * @param newNonStemProbabilityOfDying - the new probability of dying for non stem cells
     */
    public void updateCellTraits(int newGeneralCct, int newGeneralMotilitySpeed, double newStemProbabilityOfDaughterIsStem, int newNonStemMaxProliferation,  double newNonStemProbabilityOfDying){
        if (this.generalCct != newGeneralCct){
            this.generalCct = newGeneralCct;
            this.cellTraitsJustUpdated = true;
        }
        if (this.generalMotilitySpeed != newGeneralMotilitySpeed){
            this.generalMotilitySpeed = newGeneralMotilitySpeed;
            this.cellTraitsJustUpdated = true;
        }
        if (this.stemProbabilityOfDaughter != newStemProbabilityOfDaughterIsStem){
            this.stemProbabilityOfDaughter = newStemProbabilityOfDaughterIsStem;
            this.cellTraitsJustUpdated = true;
        }
        if (this.nonStemMaxProliferation != newNonStemMaxProliferation){
            this.nonStemMaxProliferation = newNonStemMaxProliferation;
            this.cellTraitsJustUpdated = true;
        }
        if (this.nonStemProbabilityOfDying != newNonStemProbabilityOfDying){
            this.nonStemProbabilityOfDying = newNonStemProbabilityOfDying;
            this.cellTraitsJustUpdated = true;
        }
    }

    /**
     * Updates the trait vector of currently active cells in the cellWatchList
     */
    private void updateTraitVectorsOfCellsInWatchList(){
        for (Point cell_coordinates: this.cellWatchlist) {
            AliveCell cell = this.getLivingCell(cell_coordinates);
            cell.setCct(this.generalCct);
            cell.setMotilitySpeed(this.generalMotilitySpeed);
            if(cell.getCellType() == "stem"){
                cell.setProbabilityOfDaughterStemCell(this.stemProbabilityOfDaughter);
            } else {
                cell.setMaxProliferation(this.nonStemMaxProliferation);
                cell.setProbabilityOfDying(this.nonStemProbabilityOfDying);
            }
            cell.updateProbabilityOfDividing();
            cell.updateProbabilityOfMigrating();
        }
    }

    /**
     * Takes alive cells that were removed from cellWatchList because they were surrounded
     * and returns them to cellWatchList if they are no are longer surrounded
     */
    public void addUnsurroundedAliveCellsIfExistToWatchList() {
        ArrayList<Point> cells_returned_to_watchlist = new ArrayList<>();
        for(Point cell_coordinates: this.surrounded_living_cells){
            if (this.hasEmptyAdjacentSpot(cell_coordinates)){
                this.cellWatchlist.add(cell_coordinates);
                cells_returned_to_watchlist.add(cell_coordinates);
            }
        }
        this.surrounded_living_cells.removeAll(cells_returned_to_watchlist);
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
            rgb = new Color(0, 0, 255).getRGB();; //blue
        } else if (cell_type.equals("dead")){
            rgb = new Color(0, 0, 0).getRGB(); //black
        }
        this.setRGB(x, y, rgb);
    }

    /**
     * @param cell_coords - the coordinates of the cell
     * @return true or false depending on whether the cell has an adjacent spot
     */
    private boolean hasEmptyAdjacentSpot(Point cell_coords){
        Point adjacent_spot = this.getEmptyAdjacentSpot(cell_coords);
        if (adjacent_spot != null){
            return true;
        } else {
            return false;
        }
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
     * @param coordinates - an arraylist of points to randomly pick from
     * @return a random point
     */
    private Point getRandomPointUsingMonteCarloSampling(ArrayList<Point> coordinates){
        int numChoices = coordinates.size();
        Random rand = new Random();
        double pick = rand.nextDouble();
        double higher_end = 1;
        double lower_end = 1 - (double) 1/numChoices;
        int chosenOption = numChoices - 1;
        for (int index = numChoices - 1; index >= 0; index = index - 1){
            chosenOption = index;
            if (pick < higher_end && pick > lower_end){
                break;
            } else {
                higher_end = higher_end - (double) 1/numChoices;
                lower_end = lower_end - (double) 1/numChoices;
            }
        }
        return coordinates.get(chosenOption);
    }


    /**
     * Gets coordinates of available (empty/dead) adjacent squares to a given cell
     * @param cell_coordinates the coordinates of the cell to find available squares adjacent to
     * @return coordinates of available adjacent squares
     */
    private ArrayList<Point> getAvailableCoordinates(Point cell_coordinates){
        ArrayList<Point> all_eight_neighbors = this.getAllEightAdjacentCoordinates(cell_coordinates);
        ArrayList<Point> neighbors_in_bounds = this.removeNeighborsOutOfBounds(all_eight_neighbors);
        ArrayList<Point> available_squares = this.removeLivingNeighbors(neighbors_in_bounds);
        return available_squares;
    }

    /**
     * @param neighbors - ArrayList of neighbor coordinates in bounds of lattice
     * @return neighbors - an ArrayList of coordinates of only empty and dead neighbors
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
     * @param neighbors - an ArrayList of points
     * @return an ArrayList of points within the bounds of the lattice
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
     * @param cell_coords - coordinates of the dividing/migrating cell
     * @return an ArrayList of the 8 adjacent points around the given point
     */
    private ArrayList<Point> getAllEightAdjacentCoordinates(Point cell_coords){
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