# iteratively download
while read p; do
  wget -e robots=off -R "index.html*" -N -nH -l inf -r --no-parent "$p"
done < websites.txt 

# recursively unzip
find . -name "*.zip" | while read filename; do unzip -o -d "`dirname "$filename"`" "$filename"; done;

# delete unzip
find . -name "*.zip" -type f -delete

# put them under the same folder
# find . -name '*.cha' -exec mv {} data/ \;

