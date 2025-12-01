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

    private Integer handleOverFlow(Integer value){
        if (value < 0) value += 100;
        if (value > 99) value -= 100;
        this.passThroughZero++;
        return value;

    }

    public Integer applyRotation(Integer currentValue){
        int value = switch (this.direction.toLowerCase()) {
            case "r" -> currentValue + this.rotation;
            case "l" -> currentValue - this.rotation;
            default -> throw new IllegalArgumentException("Invalid direction");
        };

        while (value > 99 || value < 0){
            value = this.handleOverFlow(value);
        }


//        while (value > 99){
////            for(int i = 0; i < 100; i++){
////                if(value % 100 == 0) this.passThroughZero++;
////                value --;
////            }
////            if(currentValue == 0) this.passThroughZero--;
//            value -= 100;
//            this.passThroughZero++;
//        }
//        while (value < 0){
////            for(int i = 0; i < 100; i++){
////                if(value % 100 == 0) this.passThroughZero++;
////                value ++;
////            }
////            if(currentValue == 0) this.passThroughZero--;
//            value += 100;
//            this.passThroughZero++;
//        }

//        if(this.passThroughZero == 0 && value == 0) this.passThroughZero++;
        if(this.passThroughZero != 0 && currentValue == 0) this.passThroughZero--;

        System.out.println("-------------------------------------");
        System.out.println("The dial starts by pointing at " + currentValue);
        System.out.println("The dial is rotated " + this.direction + this.rotation + " to point at " + value);
        System.out.println("During this rotation, it points at 0 " + this.passThroughZero + " times.");

        return value;
    }
}
