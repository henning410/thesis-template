import os
import sys

def search_files(directory, search_string):
    filenames = []
    line_numbers = []
    lines = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            filename = os.path.join(root, file)
            with open(filename, 'r') as f:
                for line_number, line in enumerate(f, start=1):
                    if search_string in line:
                        filenames.append(filename)
                        line_numbers.append(line_number)
                        lines.append(line.strip())

    return filenames, line_numbers, lines

def main():
    # Check if the user provided a directory and search string arguments
    if len(sys.argv) != 3:
        print("Usage: {} <directory> <search_string>".format(sys.argv[0]))
        sys.exit(1)

    search_dir = sys.argv[1]
    search_string = sys.argv[2]

    # Check if the directory exists
    if not os.path.isdir(search_dir):
        print("Directory '{}' does not exist.".format(search_dir))
        sys.exit(1)

    print("Searching for '{}' in files within directory: {}".format(search_string, search_dir))
    filenames, line_numbers, lines = search_files(search_dir, search_string)
    print("")

    if not filenames:
        print("No occurrences of '{}' found in files within directory: {}".format(search_string, search_dir))
        sys.exit(0)

    max_filename_length = max(len(os.path.basename(filename)) for filename in filenames)
    print("Filename{}Line Numbers   Matched Line".format(' ' * (max_filename_length - 7)))
    print("-" * (max_filename_length + 36))

    for filename, line_number, line in zip(filenames, line_numbers, lines):
        print("{:<{}} {:>12}    {}".format(os.path.basename(filename), max_filename_length, line_number, line))

if __name__ == "__main__":
    main()
