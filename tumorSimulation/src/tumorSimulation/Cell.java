/**
 * Cell.java
 * Alec Wang and Bat-Orgil Batjargal, 11/19/18.
 *
 * A java class for a cell, which can take the form of an empty, dead, stem or non-stem cell.
 */

package tumorSimulation;

public class Cell {
    private String cellType;

    /**
     * Creates a new cell
     */
    public Cell() {

    }

    /** Gets the current cell-type
     * @return cellType - the cell's cell-type
     */
    public String getCellType() {
        return this.cellType;
    }

    /** Sets a cell-type
     * @param newCellType - the new cell-type for the cell
     */
    public void setCellType(String newCellType) {
        this.cellType = newCellType;
    }
}

