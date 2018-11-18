/**
 * NonStemCell.java
 * Alec Wang and Bat-Orgil Batjargal, 11/19/18.
 *
 * A java class for a non-stem cell
 */

package tumorSimulation;

public class NonStemCell extends AliveCell {


    public NonStemCell(){
        this (24, 10, 5, 0.01);
    }

    public NonStemCell(int cct, int MaxProliferation, int MotilitySpeed, double ProbabilityOfDying){
        this.setCellType("non-stem");
        this.setCct(cct);
        this.setMaxProliferation(MaxProliferation);
        this.setMotilitySpeed(MotilitySpeed);
        this.setProbabilityOfDying(ProbabilityOfDying);
        this.setProbabilityOfDaughterStemCell(0);
        this.updateProbabilityOfDividing();
        this.updateProbabilityOfMigrating();
    }

    /** Non-stem cells have a {0%} chance of creating a non-stem cell
     * @return the cell-type of the daughter (either stem or non-stem)
     */
    @Override
    public String getCellTypeOfNewDaughter(){
        return("non-stem");
    }

}