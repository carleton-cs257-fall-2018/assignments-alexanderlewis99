/**
 * Cell.java
 * Alec Wang and Bat-Orgil Batjargal, 11/16/18.
 *
 * A java class for a cell, which can take the form of an empty, dead, stem or non-stem cell.
 */

package tumorSimulation;
import java.util.Random;
import java.util.HashMap;
import java.util.Map;

public class Cell {
    private String cellType;

    /**
     * Creates a new cell
     */
    public Cell() {

    }

    /**
     * @return cellType - the cell's cell-type
     */
    public String getCellType() {
        return this.cellType;
    }

    public void setCellType(String newCellType) {
        this.cellType = newCellType;
    }
}

