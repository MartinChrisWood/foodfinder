# Utilities for helping to display data
import numpy as np


def html_table(df):
    """ Formats the information nicely for display purposes. """
    # Ranks, indexed from 1 for readability
    df_out = df.assign(rank=range(len(df)))
    df_out["rank"] = df_out["rank"] + 1

    # Handles missing contact details
    df_out = df_out.fillna("")
    
    # Replace newline characters with html break
    df_out['opening'] = df_out['opening'].str.replace("\r", "")
    df_out['opening'] = df_out['opening'].str.replace("\n", "<br>")

    # Tidy name and id number into one column
    df_out['name'] = "<b>" + df_out['rank'].astype(str) + "</b> - " + df_out['name']

    # Reformat the contact links into one field, for compact display
    df_out['email'] = "Email: " + '<a href="mailto:' + df_out['email'] + '">' + df_out['email'] + '</a>'
    df_out['website'] = "Website: " + '<a href="' + "https://" +  df_out['website'] + '">' + df_out['website'] + "</a>"
    df_out['phone'] = "Phone: " + '<a href="tel:' + df_out['phone'].str.replace('0', '') + '">' + df_out['phone'] + "</a>"
    df_out['contact'] = df_out.apply(lambda row: "<br>".join([row['website'], row['email'], row['phone']]), axis=1)

    # Reformat address and postcode into one field, for compact display
    df_out['address'] = df_out['address'] + "<br>" + df_out['postcode']

    # Mark metadata clearly
    df_out['referral_required'] = np.where(df['referral_required'], "Yes", "")
    df_out['delivery_option'] = np.where(df['delivery_option'], "Yes", "")

    df_out['information'] = np.where(df['referral_required'],
                                     "Referral needed",
                                     "")
    
    df_out['information'] = np.where(df['delivery_option'],
                                     df_out['information'] + "<br><hr>Makes deliveries",
                                     df_out['information'])
    
    # Format table column heads for readability
    df_out = df_out.rename(
        columns={"referral_required": "referral", "delivery_option": "delivery", "rank": "number"}
    )[
        [
            "name",
            "address",
            "opening",
            "contact",
            "information"
        ]
    ]
    df_out.columns = [col.capitalize() for col in df_out.columns]

    return df_out.to_html(
        classes="table table-striped table-bordered table-sm table-hover",
        index=False,
        escape=False,
        render_links=True
    )
