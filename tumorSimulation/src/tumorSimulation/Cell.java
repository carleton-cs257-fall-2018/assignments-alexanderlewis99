/**
 * Cell.java
 * Alec Wang and Bat-Orgil Batjargal, 11/19/18.
 *
 * A java class for a cell, which can take the form of an empty, dead, stem or non-stem cell.
 */

package tumorSimulation;

public class Cell {
    private String cellType;

    public Cell() {

    }

    public String getCellType() {
        return this.cellType;
    }

    public void setCellType(String newCellType) {
        this.cellType = newCellType;
    }
}

