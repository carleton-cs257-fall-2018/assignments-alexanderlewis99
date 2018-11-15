package tumorSimulation;
import javax.lang.model.type.NullType;
import java.lang.reflect.Array;
import java.util.ArrayList;
import java.awt.Point;
import java.util.Map;
import java.util.Random;

public class Lattice  {

    private ArrayList<ArrayList> latticeMatrix = new ArrayList<ArrayList>();
    private int numRows;
    private int numColumns;
    private int timestep;
    private ArrayList<Point> dynamic_cells = new ArrayList<Point>();

    public Lattice(int rows, int columns){
        this.numRows = rows;
        this.numColumns = columns;
        this.timestep = 0;
        for (int i = 0; i < rows; i++){
            ArrayList<Cell> lattice_row = new ArrayList<Cell>();
            for (int j = 0; j < columns; j++){
                lattice_row.add(new Cell());
            }
            this.latticeMatrix.add(lattice_row);
        }
        int center_x = columns/2;
        int center_y = columns/2;
        Point first_stem_cell_coords = new Point(center_x, center_y);
        Cell first_stem_cell = new Cell("stem");
        this.setCell(first_stem_cell_coords, first_stem_cell);
        this.dynamic_cells.add(new Point(center_x, center_y));
    }

    /*** Get the number of rows in the lattice
     * @return number of rows
     */
    public int getNumRows(){
        return this.numRows;
    }

    /** Get the number of columns in the lattice
     * @return number of columns
     */
    public int getNumCols(){
        return this.numColumns;
    }

    /** Get a row of cells of the lattice
     * @param row_index - the index of the row which you wish to get
     * @return an arraylist of cells in the lattice
     */
    private ArrayList<Cell> getRow(int row_index){
        return this.latticeMatrix.get(row_index);
    }

    /** Set a row of the lattice as a row of cells
     * @param row_index - the index of the row which you wish to replace
     * @param new_row - a list of cells to be the new row
     * @throws IllegalArgumentException
     */
    public void setRow(int row_index, ArrayList<Cell> new_row){
        latticeMatrix.set(row_index, new_row);
        if (new_row.size() != this.numColumns) {
            throw new IllegalArgumentException();
        }
    }

    /** Get a cell from the lattice
     * @param cell_coordinates - the coordinates of the cell to get
     * @return the cell from the lattice
     */
    public Cell getCell(Point cell_coordinates){
        int x = (int) cell_coordinates.getX();
        int y = (int) cell_coordinates.getY();
        ArrayList<Cell> lattice_row = this.latticeMatrix.get(y);
        Cell cell = lattice_row.get(x);
        return cell;
    }

    /** Replace a cell in the lattice with a new cell
     * @param cell_coordinates - the coordinates of the cell to replace
     * @param new_cell - the new cell that will replace the old cell
     */
    public void setCell(Point cell_coordinates, Cell new_cell){
        int x = (int) cell_coordinates.getX();
        int y = (int) cell_coordinates.getY();
        ArrayList<Cell> lattice_row = this.latticeMatrix.get(y);
        lattice_row.set(x, new_cell);
        this.latticeMatrix.set(y, lattice_row);
    }

    /**
     * Iterates through the cellArray, receives the behavior of each cell, and acts upon it.
     */
    public void updateCells(){
        System.out.println(timestep);
        this.timestep++;
        ArrayList<Point> new_cell_to_keep_track_of = new ArrayList<Point>();
        for (Point cell_coords: this.dynamic_cells) {
            Cell cell = this.getCell(cell_coords);
            if (cell.getCellType() == "stem" || cell.getCellType() == "non-stem"){
                Map<String, Boolean> behavior = cell.live();
                System.out.println(cell_coords);
                System.out.println(behavior);
                if(behavior.get("die")){
                    cell.setGenericCellType("dead");
                }
//                    else { //migrate and divide are time-step independent
//                        if(behavior.get("migrate")){
//                            migrateCell(cell_coords);
//                        }
//                        if(behavior.get("divide")){
//                            divideCell(cell_coords);
//                        }
//                    }
            }
        }
    }


    /** Gets coordinates of available (empty/dead) adjacent squares to a given cell
     * @param cell_coordinates the coordinates of the cell to find available squares adjacent to
     * @return coordinates of available adjacent squares
     */
    private ArrayList<Point> getAvailableCoordinates(Point cell_coordinates){
        ArrayList<Point> all_eight_neighbors = this.getPotentialNeighborsCoords(cell_coordinates);
        ArrayList<Point> neighbors = this.removeNeighborsOutOfBounds(all_eight_neighbors);
        ArrayList<Point> available_squares = this.removeLivingCells(neighbors);
        return available_squares;
    }

    /** Removes coordinates of stem or non-stem cell
     * @param neighbors - ArrayList of neighbor coordinates in bounds of lattice
     * @return neighbors - an ArrayList of coordinates of empty/dead neighbors
     */
    private ArrayList<Point> removeLivingCells(ArrayList<Point> neighbors){
        for (Point neighbor_coordinate: neighbors){
            Cell cell = this.getCell(neighbor_coordinate);
            if (cell.getCellType().equals("stem") || cell.getCellType().equals("non-stem")){
                neighbors.remove(neighbor_coordinate);
            }
        }
        return neighbors;
    }

    /** Generate possible 8 neighbors coordinates
     * @param cell_coords - coordinates of the dividing/migrating cell
     * @return an ArrayList of all adjacent, including ones outside the bounds of the lattice
     */
    private ArrayList<Point> getPotentialNeighborsCoords(Point cell_coords){
        int x = (int) cell_coords.getX();
        int y = (int) cell_coords.getY();
        ArrayList<Point> all_eight_neighbors = new ArrayList<Point>();
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

    /** Removes generated imposible coordinates
     * @param neighbors - an ArrayList of Points
     * @return an ArrayList of Points
     */
    private ArrayList<Point> removeNeighborsOutOfBounds(ArrayList<Point> neighbors){
        ArrayList<Point> neighbors_to_remove = new ArrayList<Point>();
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

    /** Gets a random point from a set of points using Monte Carlo sampling
     * @param coordinates - an arraylist of points to sample from
     * @return a random coordinate
     */
    private Point getRandomPointUsingMonteCarloSampling(ArrayList<Point> coordinates){
        int numChoices = coordinates.size();
        Random rand = new Random();
        double chance = rand.nextDouble();
        double higher_end = 1;
        double lower_end = 1 - (double) 1/numChoices;
        for (int chosenOption = numChoices; chosenOption >= 0; chosenOption = chosenOption - 1){
            if (chance < higher_end && chance > lower_end){
                return coordinates.get(chosenOption);
            } else {
                higher_end = higher_end - (double) 1/numChoices;
                lower_end = lower_end - (double) 1/numChoices;
            }
        }
        return coordinates.get(0); //unnecessary because when lower_end reaches 0, the if statement in the for loop will be true
    }

    /** Finds an empty adjacent square in the lattice to a cell if one exists
     * @param cell_coords - the coordinates of the cell
     * @return the coordinates of the empty adjacent square
     */
    private Point getEmptyAdjacentSpot(Point cell_coords){
        ArrayList<Point> avaliableCoords = getAvailableCoordinates(cell_coords);
        if (avaliableCoords.size() > 0){
            return null;
        }
        Point new_coords = getRandomPointUsingMonteCarloSampling(avaliableCoords);
        return new_coords;
    }

    /** Divides a cell by finding an empty neighbor to become a daughter cell
     * @param cell_coords - the coordinates of the cell to divide
     * @return the coordinates of the new daughter cell
     */
    private Point divideCell(Point cell_coords){
        return new Point(0,0);
    }


}