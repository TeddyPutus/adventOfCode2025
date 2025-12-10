puts "Day 9"

filepath = "YOUR_FILEPATH"

class Tile
  @x
  @y

  def initialize(x, y)
    @x = x
    @y = y
  end

  def getX()
    @x
  end

  def getY()
    @y
  end
end

def get_area(tile_1, tile_2)
  ((tile_2.getX - tile_1.getX).abs + 1) * ((tile_2.getY - tile_1.getY).abs + 1)
end

tiles = []

File.readlines(filepath, chomp: true).each do |line|
  puts(line)
  line.strip!
  coords = line.split(",")
  tiles.append(Tile.new(coords[0].to_i, coords[1].to_i))
end

max_area = 0
max_tiles = []

tiles.combination(2).each do |tile|
  area = get_area(tile[0], tile[1])
  if area > max_area
    max_area = area
    max_tiles = tile
  end
end

puts "Answer is #{max_area} using tiles (#{max_tiles[0].getX}, #{max_tiles[0].getY}) and (#{max_tiles[1].getX}, #{max_tiles[1].getY})"