This project contains the data on open source libraries and licenses used in XL products.

# Generating a license overview

The following command can be used to generate a CSV file with libraries and licenses:

    cat src/main/resources/license-data.json | jq '.artifacts|with_entries(.value = .value["license"])|to_entries|map(.key + "," + .value)|.[]' > ~/tmp/licenses.csv

# Generating a license list for Bart Valk

Bart will reach out to generate new overviews of libraries and their licenses which are included in our products. Using a script these can be generated from an unzipped distribution.

    $ python3 generate-list.py <XLD_SERVER_HOME>/lib > output.txt
