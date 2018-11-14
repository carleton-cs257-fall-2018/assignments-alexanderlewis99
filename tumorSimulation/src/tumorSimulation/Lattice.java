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

    public Lattice(int rows, int columns){
        this.numRows = rows;
        this.numColumns = columns;
        for (int i = 0; i < rows; i++){
            ArrayList<Cell> lattice_row = new ArrayList<Cell>();
            for (int j = 0; j < columns; j++){
                lattice_row.add(new Cell());
            }
            this.latticeMatrix.add(lattice_row);
        }
    }

    public int getNumRows(){
        return this.numRows;
    }

    public int getNumCols(){
        return this.numColumns;
    }

    private ArrayList<Cell> getRow(int row_index){
        return this.latticeMatrix.get(row_index);
    }

    public void setRow(int index, ArrayList<Cell> new_row){
        latticeMatrix.set(index, new_row);
    }

    public Cell getCell(int x, int y){
        ArrayList<Cell> lattice_row = this.latticeMatrix.get(y);
        Cell cell = lattice_row.get(x);
        return cell;
    }

    public void setCell(int x, int y, Cell new_cell){
        ArrayList<Cell> lattice_row = this.latticeMatrix.get(y);
        lattice_row.set(x, new_cell);
        this.latticeMatrix.set(y, lattice_row);
    }

    /**
     * Iterates through the cellArray, receives the behavior of each cell, and acts upon it.
     */
    public void updateCells(){
        for(int y = 0; y < this.numRows; y++){
            ArrayList<Cell> row = this.getRow(y);
            for(int x = 0; x < this.numColumns; x++) {
                Cell cell = row.get(x);
                Point cell_coords = new Point(x, y);
                if (cell.getCellType() == "stem" || cell.getCellType() == "non-stem"){
                    Map<String, Boolean> behavior = cell.live();
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
            int x = (int) neighbor_coordinate.getX();
            int y = (int) neighbor_coordinate.getX();
            Cell cell = this.getCell(x, y);
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