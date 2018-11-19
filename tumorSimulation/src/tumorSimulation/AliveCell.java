/**
 * AliveCell.java
 * Alec Wang and Bat-Orgil Batjargal, 11/19/18.
 *
 * A java class for a living cell
 */

package tumorSimulation;
import java.util.Random;
import java.util.HashMap;
import java.util.Map;

public class AliveCell extends Cell {
    private final double timestep = (double) 1/24;
    private int cct; //cell cycle time (affects the rate which a cell divides)
    private int max_proliferation;    //max times the cell can divide before dying
    private double motility_speed; //migration potential (affects the rate at which a cell migrates)
    private double probability_of_dying;    //rate of spontaneous death (probability each timestep it spontaneously dies)
    private double probability_of_daughter_stem_cell; //the probability that a new daughter cell is also a stem cell (for stem cells only)
    private double probability_of_dividing;
    private double probability_of_migrating;

    public AliveCell(){

    }

    public int getCct() {
        return this.cct;
    }


    public void setCct(int new_cct) {
        this.cct = new_cct;
    }


    public int getMaxProliferation() {
        return this.max_proliferation;
    }


    public void setMaxProliferation(int new_max_proliferation) {
        this.max_proliferation = new_max_proliferation;
    }


    public double getProbabilityOfDying() {
        return this.probability_of_dying;
    }


    public void setProbabilityOfDying(double new_probability_of_dying) {
        this.probability_of_dying = new_probability_of_dying;
    }

    public double getMotilitySpeed() {
        return this.motility_speed;
    }


    public void setMotilitySpeed(double new_motility_speed) {
        this.motility_speed = new_motility_speed;
    }


    public double getProbabilityOfDaughterStemCell() {
        return this.probability_of_daughter_stem_cell;
    }


    public void setProbabilityOfDaughterStemCell(double new_probability_of_daughter_stem_cell) {
        this.probability_of_daughter_stem_cell = new_probability_of_daughter_stem_cell;
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
     * @return the cell-type of the daughter (either stem or non-stem)
     */
    public String getCellTypeOfNewDaughter(){
        Random rand = new Random();
        double chance = rand.nextDouble();
        if (chance <= this.probability_of_daughter_stem_cell){
            return ("stem");
        }
        else {
            return("non-stem");
        }
    }

    public Map<String, Boolean> getBehaviorForTimestep() {
        Map<String, Boolean> behavior = new HashMap<String, Boolean>();
        behavior.put("migrate", this.migrateIfChanceAllows());
        behavior.put("divide", this.divideIfChanceAllows());
        behavior.put("die", this.dieIfUnlucky());
        return behavior;
    }

    /**
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