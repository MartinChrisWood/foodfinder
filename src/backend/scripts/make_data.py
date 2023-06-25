import os
import pandas as pd
import requests
import toml
from zipfile import ZipFile


def postcode_to_coords(DATA_DIR):

    """Ingests and processes postcodes and coordinates for
    all postcodes in Sheffield district
    """

    URL = "http://download.geonames.org/export/zip/GB_full.csv.zip"
    filename = URL.split("/")[-1]
    filepath = f"{DATA_DIR}/{filename}"
    r = requests.get(URL)

    if r.ok:
        with open(filepath, "wb") as f:
            f.write(r.content)

            with ZipFile(f"{filepath}", "r") as zip:
                    for info in zip.infolist():
                        if not os.path.exists(f"{DATA_DIR}/{info.filename}"):
                            zip.extract(info, f"{DATA_DIR}")
                            print(f"Saved {info.filename}")
                        else:
                            print(f"{info.filename} already exists")
        r.close()
        print("Ingest complete")

    gb_postcodes = pd.read_csv(f"{DATA_DIR}/GB_full.txt", sep="\t", header=None)
    gb_postcodes = gb_postcodes.iloc[:, 1:-1]
    gb_postcodes.columns = ["postcode",
                            "area",
                            "country",
                            "country_code",
                            "region",
                            "blank",
                            "district",
                            "district_code",
                            "lat",
                            "long"]
    gb_postcodes.drop(columns="blank", inplace=True)

    # 13407 postcodes in Sheffield District
    # 1143 postcodes in Sheffield District not classified as Sheffield area
    shef_postcodes = gb_postcodes[(gb_postcodes["area"]=="Sheffield")|
                                (gb_postcodes["district"].str.contains("Sheffield"))].reset_index(drop=True)

    # Remove spaces
    shef_postcodes['postcode'] = shef_postcodes['postcode'].str.replace(" ", "")

    shef_postcodes.to_csv(f"{DATA_DIR}/shef_pc_coords_lookup.csv")
    print("Lookup file exported")
    return shef_postcodes


def foodbank_coords(DATA_DIR, pc_data):
    """Assigns coordinates to foodbank postcodes and
    tidies formatting
    """
    foodbanks = pd.read_csv(f"{DATA_DIR}/foodbanks.csv")
    foodbanks.rename(columns={"Postcode": "postcode"}, inplace=True)
    foodbanks['postcode'] = foodbanks['postcode'].str.replace(" ", "")
    foodbanks = pd.merge(foodbanks, pc_data[["postcode", "lat", "long"]], on="postcode")
    foodbanks.columns = foodbanks.columns.str.lower()
    foodbanks = foodbanks.reset_index(names="ID")

    # Clean up text columns
    foodbanks['name'] = foodbanks['name'].str.strip()
    foodbanks['address'] = foodbanks['address'].str.strip()

    foodbanks.to_csv(f"{DATA_DIR}/foodbank_coords.csv", index=False)
    return None



def main():
     
    # Load config
    with open("pipeline.toml", "r") as f:
        config = toml.load(f)

    DATA_DIR = config["DATA_DIR"]
    pc_data = postcode_to_coords(DATA_DIR)
    foodbank_coords(DATA_DIR, pc_data)


if __name__=="__main__":
    main()



