using System;

public class Connection
{
	public double distance;
	public JunctionBox start;
	public JunctionBox end;

	public Connection(JunctionBox start, JunctionBox end)
	{
		this.start = start;
		this.end = end;
		this.distance = this.calculateDistance();
	}

	public double calculateDistance()
    {
        float dx = this.start.x - this.end.x;
        float dy = this.start.y - this.end.y;
        float dz = this.start.z - this.end.z;

        return Math.Sqrt(dx * dx + dy * dy + dz * dz);

    }
}
