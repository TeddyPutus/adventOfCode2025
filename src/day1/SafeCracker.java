package day1;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class SafeCracker {
    private final String filepath;
    private Integer currentPoint;
    private Integer landOnZero;
    private Integer passThroughZero;

    public SafeCracker(String filepath,  Integer startPoint){
        this.filepath = filepath;
        this.currentPoint = startPoint;
        this.landOnZero = 0;
        this.passThroughZero = 0;
    }

    public void crackSafe(){
        try (BufferedReader br = new BufferedReader(new FileReader(this.filepath))) {
            String line;
            while ((line = br.readLine()) != null) {
                Rotation rotation = new Rotation(line.strip());
                this.currentPoint = rotation.applyRotation(this.currentPoint);
                if(this.currentPoint == 0){
                    this.landOnZero++;
                }
                this.passThroughZero += rotation.getPassThroughZero();
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public Integer getPassThroughZero() {
        return this.passThroughZero;
    }

    public Integer getLandOnZero() {
        return this.landOnZero;
    }
}
