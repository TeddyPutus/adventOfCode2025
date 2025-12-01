package day1;

import static java.lang.Integer.parseInt;

public class Rotation {
    private final String direction;
    private final Integer rotation;
    private Integer passThroughZero;

    public Rotation(String r){
        this.direction = getDirection(r);
        this.rotation = getRotation(r);
        this.passThroughZero = 0;
    }

    Integer getPassThroughZero() {
        return this.passThroughZero;
    }

    String getDirection(String r){
        return r.substring(0, 1);
    }

    Integer getRotation(String r){
        return parseInt(r.substring(1));
    }

    public Integer applyRotation(Integer currentValue){
        int modifier = switch (this.direction.toLowerCase()) {
            case "r" -> 1;
            case "l" -> -1;
            default -> throw new IllegalArgumentException("Invalid direction");
        };

        for (int i = 0; i < this.rotation; i++){
            currentValue += modifier;

            if(currentValue == -1) currentValue = 99;
            if(currentValue == 100) currentValue = 0;

            if(currentValue == 0) this.passThroughZero++;
        };

        System.out.println("-------------------------------------");
        System.out.println("The dial is rotated " + this.direction + this.rotation + " to point at " + currentValue);
        System.out.println("During this rotation, it points at 0 " + this.passThroughZero + " times.");

        return currentValue;
    }
}
