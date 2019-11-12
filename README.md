This project contains the data on open source libraries and licenses used in XL products.

# Generating a license overview

The following command can be used to generate a CSV file with libraries and licenses:

    cat src/main/resources/license-data.json | jq '.artifacts|with_entries(.value = .value["license"])|to_entries|map(.key + "," + .value)|.[]' > ~/tmp/licenses.csv

# Generating a license list for Bart Valk

Bart will reach out to generate new overviews of libraries and their licenses which are included in our products. Using a script these can be generated from an unzipped distribution.

    $ python3 generate-list.py <XLD_SERVER_HOME>/lib > output.txt

# Generating an Excel file for our legal department

On 11 and 12 november 2019 in an email chain involving me (Jasper Stein), Mayur Patel, Benjamin Rosen, Martin O'Keefe, Christian
van den Branden, Mike McKechnie it was determined that we want an `.xlsx` sheet with an overview of OSS licenses we use, on each
version of XLD and XLR we release. To aid the creation of this some more, the following script will produce a `.csv` file that
Microsoft Excel will know how to parse, so it is easy to let it turn it into an `.xlsx` file for upload to, e.g., 
https://xebialabs.app.box.com/folder/86224075625 for XL Deploy or https://xebialabs.app.box.com/folder/86223755194 for XL Release

    $ python3 generate-csv.py <XLD_SERVER_HOME>/lib <outputfile>