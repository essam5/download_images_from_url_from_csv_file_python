import os
import sys
import urllib.request
import urllib
import csv

try:
    filename = "products.csv"
    url_name = "image_link"
except:
    print("\nERROR: Please specify filename and url column name to download\n")
    print("Usage:")
    print(" $ picodash_export_url_download.py data.csv image_url\n")
    print("- First param should be the csv file path")
    print("- Second param should be the column name that has image urls to download\n")
    sys.exit(0)

# open csv file to read
with open(filename, "r") as csvfile:
    csv_reader = csv.reader(csvfile)
    # iterate on all rows in csv
    for row_index, row in enumerate(csv_reader):
        # find the url column name to download in first row
        if row_index == 0:
            IMAGE_URL_COL_NUM = None
            for col_index, col in enumerate(row):
                if col == url_name:
                    IMAGE_URL_COL_NUM = col_index
            if IMAGE_URL_COL_NUM is None:
                print(
                    "\nERROR: url column name '"
                    + url_name
                    + "' not found, available options:"
                )
                for col_index, col in enumerate(row):
                    print(" " + col)
                print("\nUsage:")
                print(" $ picodash_export_url_download.py data.csv image_url\n")
                sys.exit(0)
            continue
        # check if we have an image URL and download in rows > 1
        image_urls = row[IMAGE_URL_COL_NUM]
        image_urls = image_urls.split("\n")
        # print image_urls
        for image_url in image_urls:
            if image_url != "" and image_url != "\n":
                print(image_url)
                date = row[3].split(" ")[0]
                image_filename = row[0] + ".png"
                # image_filename = row[0] + "-" + row[1] + ".jpg"
                directory = filename.split(".csv")[0] + "-" + url_name
                if not os.path.exists(directory):
                    os.makedirs(directory)
                try:
                    urllib.request.urlretrieve(
                        image_url, directory + "/" + image_filename
                    )
                    print("[" + str(row_index) + "] Image saved: " + image_filename)
                except:
                    # second attempt to download if failed
                    try:
                        urllib.request.urlretrieve(
                            image_url, directory + "/" + image_filename
                        )
                        print("[" + str(row_index) + "] Image saved: " + image_filename)
                    except:
                        print(
                            "["
                            + str(row_index)
                            + "] Could not download url: "
                            + image_url
                        )
            else:
                print("[" + str(row_index) + "] No " + url_name)
