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
    private final double timestep = (double) 1/24;
    private String cellType;
    private int cct; //cell cycle time (affects the rate which a cell divides)
    private int max_proliferation;    //max times the cell can divide before dying
    private double motility_speed; //migration potential (affects the rate at which a cell migrates)
    private double probability_of_dying;    //rate of spontaneous death (probability each timestep it spontaneously dies)
    private double probability_of_daughter_stem_cell; //the probability that a new daughter cell is also a stem cell (for stem cells only)
    private double probability_of_dividing;
    private double probability_of_migrating;

    public Cell() {
        this("empty");
    }

    /**
     * Creates a new cell with an assigned celltype
     * @param assigned_cellType - the celltype: stem, non-stem, empty, or dead
     */
    public Cell(String assigned_cellType) {
        this.setGenericCellType(assigned_cellType);
    }

    /**
     * Causes the cell to undergo its normal behavior (dividing, migrating, and/or dying) for the timestep
     */
    public Map<String, Boolean> live() {
        Map<String, Boolean> behavior = new HashMap<String, Boolean>();
        if (this.cellType == "dead" || this.cellType == "empty") {
            behavior.put("migrate", false);
            behavior.put("divide", false);
            behavior.put("die", false);
        } else {
            behavior.put("migrate", this.migrateIfChanceAllows());
            behavior.put("divide", this.divideIfChanceAllows());
            behavior.put("die", this.dieIfUnlucky());
        }
        return behavior;
    }

    /**
     * @return cellType - the cell's cell-type
     */
    public String getCellType() {
        return this.cellType;
    }

    /**
     * Updates the cell's characteristics based on the cell-type
     * @param cellType - the new celltype: stem, non-stem, or dead
     */
    public void setGenericCellType(String cellType) {
        this.cellType = cellType;
        switch (cellType) {
            case "stem":
                this.setCellToStem();
                break;
            case "non-stem":
                this.setCellToNonStem();
                break;
            case "dead":
                this.setCellToDead();
                break;
        }
    }

    public String get_celltype_of_new_daughter(){
        Random rand = new Random();
        double chance = rand.nextDouble();
        if (chance <= this.probability_of_daughter_stem_cell){
            return ("stem");
        }
        else {
            return("non-stem");
        }
    }


    /**
     * @return max_proliferation - the number of times a cell can divide before dying
     */
    public int getMaxProliferation() {
        return this.max_proliferation;
    }

    /**
     * Sets the maximum number of times a cell can proliferate before dying
     */
    public void setMaxProliferation(int new_max_proliferation) {
        this.max_proliferation = new_max_proliferation;
    }

    /**
     * Updates the probability of the cell dividing based on its cct (cell cycle time) and the timestep
     */
    public void updateProbabilityOfDividing() {
        this.probability_of_dividing = (double)(24/this.cct) * this.timestep;
    }

    /**
     * Updates the probability of the cell migrating based on its cct (cell cycle time), motility speed and the timestep
     */
    public void updateProbabilityOfMigrating() {
        this.updateProbabilityOfDividing();
        this.probability_of_migrating = (1 - this.probability_of_dividing) * this.motility_speed  * this.timestep;
    }

    /**
     * Set the cell's characteristics to those of a stem cell
     */
    private void setCellToStem() {
        this.cct = 24;
        this.max_proliferation = -1; //proliferates infinitely
        this.probability_of_dying = 0; //immortal
        this.motility_speed = 5;
        this.probability_of_daughter_stem_cell = 0.1;
        this.updateProbabilityOfDividing();
        this.updateProbabilityOfMigrating();
    }

    /**
     * Set the cell's characteristics to those of a non-stem cell
     */
    private void setCellToNonStem() {
        this.cct = 24; //hours
        this.max_proliferation = 10;
        this.motility_speed = 5;
        this.probability_of_dying = 0.01;
        this.probability_of_daughter_stem_cell = 0;
        this.updateProbabilityOfDividing();
        this.updateProbabilityOfMigrating();
    }

    /**
     * Set the cell's characteristics to those of a dead cell
     */
    private void setCellToDead() {
        this.cct = -1;
        this.max_proliferation = -1;
        this.motility_speed = -1;
        this.probability_of_dying = 0;
        this.probability_of_daughter_stem_cell = -1;
        this.probability_of_dividing = 0;
        this.probability_of_migrating = 0;
    }

    /**
     * Causes the cell to divide if the random generated value is less than the probability of dividing
     * @return boolean - whether the cell should divide
     */
    private boolean divideIfChanceAllows(){
        Random rand = new Random();
        double chance = rand.nextDouble();
        if (chance < this.probability_of_dividing){
            return true;
        } else {
            return false;
        }
    }
    /**
     * Causes the cell to migrate if the random generated value is less than the probability of migrating
     * @return boolean - whether the cell should migrate
     */
    private boolean migrateIfChanceAllows(){
        Random rand = new Random();
        double chance = rand.nextDouble();
        if (chance < this.probability_of_migrating){
            return true;
        } else {
            return false;
        }
    }

    /**
     * Causes the cell to die if the random generated value is less than the probability of dying
     * @return boolean - whether the cell should die
     */
    private boolean dieIfUnlucky(){
        Random rand = new Random();
        double chance = rand.nextDouble();
        if (chance < this.probability_of_dying){
            return true;
        }  else {
            return false;
        }
    }
}

