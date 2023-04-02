# Remove all videos with an underscore in them in the "videos" directory

for i in $(ls videos | grep _); do
    rm videos/$i
    echo "Removed $i"
done

echo "Done!"