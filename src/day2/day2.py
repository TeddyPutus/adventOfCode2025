import re

regex_part_1 = re.compile(r"^(\d+)(\1)$")
regex_part_2 = re.compile(r"^(\d+)(\1)+$")

total = 0

if __name__ == "__main__":
    print("!!!!!!")
    with open("../../input_files/day_2.txt") as f:
        text = f.read().strip()

    for pair in text.split(","):
        start, end = pair.split("-")
        for i in range(int(start), int(end) + 1):
            # result = regex_part_1.fullmatch(str(i))
            result = regex_part_2.fullmatch(str(i))
            if result:
                print(f"{i} is invalid!")
                total += i

    print(f"Total invalid: {total}")