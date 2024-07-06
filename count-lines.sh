# Check if the directory argument is provided
if [ -z "$1" ]; then
echo "Usage: $0 <https://github.com/.../blah.git>"
exit 1
fi

cd /tmp
time=$(date +"%Y-%m-%d_%H-%M-%S")
mkdir $time
cd $time
git clone "$1" > /dev/null 2>&1

# Directory to process
DIR="."

# Check if the directory exists
if [ ! -d "$DIR" ]; then
echo "Directory $DIR does not exist."
exit 1
fi

# Calculate the total number of lines
total_lines=$(find "$DIR" -type f | grep -v .git | xargs wc -l | awk 'END {print $1}')

# Print the result
echo "$total_lines"