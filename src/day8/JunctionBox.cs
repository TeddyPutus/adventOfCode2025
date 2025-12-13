using System;
using System.Security.Cryptography.X509Certificates;

public class JunctionBox
{
	public long x;
	public long y;
	public long z;
    public bool visited = false;

    public List<JunctionBox> circuit = new List<JunctionBox>();

	public JunctionBox(long x, long y, long z)
	{
		this.x = x;
		this.y = y;
		this.z = z;
        this.circuit.Add(this);
	}

    public String getKey()
    {
        return $"{this.x},{this.y},{this.z}";
    }

    public void connect(JunctionBox box, bool shouldCheck = true)
    {
        this.circuit.Add(box);
        this.circuit = this.circuit.Distinct().ToList();
    }

    public int circuitSize() {

        if (this.visited) return 0;
        else
        {
            this.visited = true;
            return 1 + this.circuit.Select(j => j.circuitSize()).Sum();
        }

    }

    public void resetVisited()
    {
        if (!this.visited) return;
        else
        {
            this.visited = false;
            this.circuit.ForEach(j => j.resetVisited());
        }

    }

}
