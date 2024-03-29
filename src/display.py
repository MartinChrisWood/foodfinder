# Utilities for helping to display data
import numpy as np


def create_collapsible_element(cover: str, content: str) -> str:
    return f"""<button type="button" class="collapsible">{cover}</button><div class="content"><p>{content}</p></div>"""


def clean_whitespace(x: str) -> str:
    """ Cleans up different whitespace characters. """
    return x.replace("\n", "<br>").replace("\r", "").strip()


def html_table(df):
    """ Formats the information nicely for display purposes. """
    # Ranks, indexed from 1 for readability
    df_out = df.assign(rank=range(len(df)))
    df_out["rank"] = df_out["rank"] + 1

    # Handles missing contact details
    df_out = df_out.fillna("")
    
    # Replace newline characters with html break
    for col in ['opening', 'email', 'phone', 'address']:
        df_out[col] = df_out[col].apply(clean_whitespace)

    # Tidy name, id number, address and postcode into one column
    df_out['name'] = "<b>" + df_out['rank'].astype(str) + " - " + df_out['name'] + "</b><br>" +\
        df_out['address'].str.replace("\n", "<br>").str.replace("\r", "") + "<br>" + df_out['postcode']

    # Reformat the contact links into one field, for compact display
    df_out['email'] = "Email: " + '<a href="mailto:' + df_out['email'] + '">' + df_out['email'] + '</a>'
    df_out['website'] = "Website: " + '<a href="' + "https://" +  df_out['website'] + '">' + df_out['website'] + "</a>"
    df_out['phone'] = "Phone: " + '<a href="tel:' + df_out['phone'].str.replace('0', '') + '">' + df_out['phone'] + "</a>"
    df_out['contact'] = df_out.apply(lambda row: "<br>".join([row['website'], row['email'], row['phone']]), axis=1)

    # Mark metadata clearly
    df_out['referral_required'] = np.where(df['referral_required'], "Yes", "")
    df_out['delivery_option'] = np.where(df['delivery_option'], "Yes", "")

    # Mark out referral link
    df_out['referral_link'] = '<a href="' + "https://" +  df_out['referral_link'] + '">' + df_out['referral_link'] + "</a>"

    df_out['information'] = "<b>" + df_out['category'] + "</b>"

    df_out['information'] = np.where(df_out['referral_required'],
                                     df_out['information'] + "<br><hr>Referral needed",
                                     df_out['information'])
    
    df_out['information'] = np.where(df_out['delivery_option'],
                                     df_out['information'] + "<br><hr>Makes deliveries",
                                     df_out['information'])

    df_out['information'] = np.where(df_out['support'].str.strip() != "",
                                     df_out['information'] + "<br><hr>" + df_out['support'].str.replace("\n", "<br>").str.replace("\r", ""),
                                     df_out['information'])
    
    
    # Format table column heads for readability
    df_out = df_out.rename(
        columns={"referral_required": "referral", "delivery_option": "delivery", "rank": "number", "referral_link": "referencing"}
    )[
        [
            "name",
            "opening",
            "contact",
            "information",
            "referencing"
        ]
    ]
    df_out.columns = [col.capitalize() for col in df_out.columns]

    return df_out.to_html(
        classes="table table-striped table-bordered table-sm table-hover",
        index=False,
        escape=False,
        render_links=True
    )
