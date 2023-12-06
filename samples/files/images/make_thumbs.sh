#!/bin/bash

# Specify the input folder containing .png files
input_folder="./src"

# Specify the output folder where resized images will be saved
output_folder="./thumbs"

# Ensure the output folder exists
mkdir -p "$output_folder"

# Loop through all .png files in the input folder
for file in "$input_folder"/*.png; do
    # Check if the file exists and is a regular file
    if [[ -f "$file" ]]; then
        # Get the filename without the extension
        filename_no_ext=$(basename -- "$file" .png)


        # 500 x 500 pixels
        output_file="$output_folder/${filename_no_ext}_500x500.jpg"
        if [[ ! -f "$output_file" ]]; then
            # Run the ImageMagick command for resizing
            convert "$file" -resize 500x500^ -gravity center -extent 500x500 "$output_file"

            echo "Resized: $file -> $output_file"
        else
            echo "Skipped: $file (output file already exists)"
        fi

        # 250 x 250 pixels
        output_file="$output_folder/${filename_no_ext}_250x250.jpg"
        if [[ ! -f "$output_file" ]]; then
            # Run the ImageMagick command for resizing
            convert "$file" -resize 250x250^ -gravity center -extent 250x250 "$output_file"

            echo "Resized: $file -> $output_file"
        else
            echo "Skipped: $file (output file already exists)"
        fi

        # 150 x 150 pixels
        output_file="$output_folder/${filename_no_ext}_150x150.jpg"
        if [[ ! -f "$output_file" ]]; then
            # Run the ImageMagick command for resizing
            convert "$file" -resize 150x150^ -gravity center -extent 150x150 "$output_file"

            echo "Resized: $file -> $output_file"
        else
            echo "Skipped: $file (output file already exists)"
        fi

    fi
done
