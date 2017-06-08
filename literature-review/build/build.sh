set -o errexit

# Generate reference information
echo "Retrieving and processing reference metadata"
# rm references/generated/bibliography.json
(cd build && python references.py)

# pandoc settings
CSL_PATH=references/nonequilibrium.csl
BIBLIOGRAPHY_PATH=references/generated/bibliography.json
INPUT_PATH=references/generated/all-sections.md

# Make output directory
mkdir -p output
# Move images to output directory
echo "Copying images"
cp -R sections/images output/

# Create HTML outpout
# http://pandoc.org/MANUAL.html
echo "Exporting HTML manuscript"
pandoc --verbose \
  --from=markdown --to=html5 \
  --filter pandoc-fignos \
  --bibliography=$BIBLIOGRAPHY_PATH \
  --metadata link-citations=true \
  --css=github-pandoc.css \
  --katex \
  --output=output/index.html \
  $INPUT_PATH

# Create PDF outpout
echo "Exporting PDF manuscript"

# The reason the images fail is because the PDF creation program
# is running inside build/ and thus looking there for images.
# But we want the path to be relative so that the HMTL file,
# served from gh-pages looks at the relative path.

cd output

pandoc --verbose \
  --from=markdown --to=html5 \
  --filter pandoc-fignos \
  --bibliography=../$BIBLIOGRAPHY_PATH \
  --csl=../$CSL_PATH \
  --metadata link-citations=true \
  --css=../output/github-pandoc.css \
  --mathml \
  --output=../output/nonequilibrium-literature-review.pdf \
  ../$INPUT_PATH

# echo "...using LaTeX"
# pandoc --verbose \
#   --from=markdown \
#   --filter pandoc-fignos \
#   --bibliography=$BIBLIOGRAPHY_PATH \
#   --csl=$CSL_PATH \
#   --metadata link-citations=true \
#   --output=output/nonequilibrium-literature-review.pdf \
#   $INPUT_PATH

