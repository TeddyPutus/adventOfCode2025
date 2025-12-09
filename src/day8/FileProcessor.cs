using System;

public class FileProcessor
{
	string filepath;
	List<JunctionBox> junctionBoxes = new List<JunctionBox>();

    public FileProcessor(string filepath)
	{
		this.filepath = filepath;
	}

	public List<JunctionBox> GetJunctionBoxes()
	{
		return this.junctionBoxes;
	}

	public List<JunctionBox> loadFile()
	{
        if (File.Exists(this.filepath))
        {
            StreamReader Textfile = new StreamReader(this.filepath);
            string line;

            while ((line = Textfile.ReadLine()) != null)
            {
                string[] coords = line.Trim().Split(',');
                this.junctionBoxes.Add(new JunctionBox(long.Parse(coords[0]), long.Parse(coords[1]), long.Parse(coords[2])));
            }

            Textfile.Close();
        }
        else
        {
            Console.WriteLine("Invalid filepath");
        }
        return this.junctionBoxes;
    }

}
