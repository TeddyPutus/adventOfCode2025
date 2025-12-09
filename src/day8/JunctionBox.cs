using System;
using System.Security.Cryptography.X509Certificates;

public class JunctionBox
{
	public long x;
	public long y;
	public long z;
    public bool visited = false;
    public bool connected = false;

    public List<JunctionBox> circuit = new List<JunctionBox>();

	public JunctionBox(long x, long y, long z)
	{
		this.x = x;
		this.y = y;
		this.z = z;
        this.circuit.Add(this);
	}

    public long connect(JunctionBox box, bool shouldCheck = true)
    {
        long result = 0;
        if ((box.connected || this.connected) && shouldCheck && !this.circuit.Contains(box) && !box.circuit.Contains(box)) {
            result = box.x * this.x;
            Console.WriteLine($"Full circuit of size ({result}) made by {box.x}, {box.y}, {box.z} -> {this.x}, {this.y}, {this.z}");
        }
        box.connected = true;
        this.circuit.Add(box);
        this.circuit = this.circuit.Distinct().ToList();
        return result;
    }

    public int circuitSize() {

        if (this.visited) return 0;
        else
        {
            this.visited = true;
            return 1 + this.circuit.Select(j => j.circuitSize()).Sum();
        }

    }

    public bool isConnected(JunctionBox box)
    {
        if (this.visited) return false;
        if(this.circuit.Contains(box)) return true;
        this.visited = true;
        return this.circuit.Select(j => j.isConnected(box)).Any(c => c == true);
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
