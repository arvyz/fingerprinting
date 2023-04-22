import os
import json
import hashlib
import random

def get_random_color():
    """
    Returns a random color in hexadecimal format
    """
    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    return color

output_dir = "./output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

head="""<!DOCTYPE html>
<html>
<head>
    <title>Output Table</title>
    <style>
"""

# Define the CSS styles as a string
css_styles = """
table {
  border-collapse: collapse;
  margin: 0 auto;
  font-size: 1em;
  font-family: sans-serif;
  min-width: 400px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
}
table thead tr {
  background-color: #1c87c9;
  color: #ffffff;
  text-align: left;
}
table th,
table td {
  padding: 3px 15px;
}
table tbody tr {
  line-height = 0;
  border-bottom: 1px solid #dddddd;
}
/*
table tbody tr:nth-of-type(even) {
  background-color: #f3f3f3;
}
*/
table tbody tr:last-of-type {
  border-bottom: 2px solid #1c87c9;
}
table tbody tr.active-row {
  font-weight: bold;
  color: #1c87c9;
}
/*
img {
    max-width: 200px;
    max-height: 200px;
}
*/
"""
head_end="""    </style>
</head>
"""

table_header = """
<table>
<tr>
<th>Fingerprint ID</th>
<th>Browser</th>
<th>Mode</th>
<th>Fingerprint Mode</th>
<th>Event</th>
<th>Date</th>
<th>Time</th>
<th>Canvas Image</th>
<th>Canvas Hash (MD5)</th>
</tr>
"""

table_footer = """
</table>
"""

table_rows = []
filelist = os.listdir(".")
for filename in filelist:
    if filename.endswith(".json"):
        with open(filename, "r") as f:
            data = json.load(f)
            filename_parts = filename.split("_")
            idx = -1

            # get the first consistent parts of the filename
            fingerprint_id = filename_parts[idx+1]
            browser = filename_parts[idx+2]
            if browser == "chrome":
                browser = '<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Google_Chrome_icon_%28February_2022%29.svg/2048px-Google_Chrome_icon_%28February_2022%29.svg.png" style="max-height: 40px; max-width: 40px;">'
            elif browser == "brave":
                browser = '<img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Brave_icon_lionface.png" style="max-height: 40px; max-width: 40px;">'
            else:
                browser = '<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Tor_Browser_icon.svg/512px-Tor_Browser_icon.svg.png?20200621064338" style="max-height: 40px; max-width: 40px;">'

            mode = filename_parts[idx+3]
            fingerprinting_mode = filename_parts[idx+4]

            # handle the fact that some filenames don't have the fingerprint mode
            if fingerprinting_mode.isdigit():
                fingerprinting_mode = ""
                idx -= 1

            # handle the fact that some file names have an another descriptor before date
            date = filename_parts[idx+5]
            event = ""
            if date.isalpha():
                event = date
                date = filename_parts[idx+6]
                idx += 1

            # get the time after removing '.json' from the name
            time = filename_parts[idx+6].split(".")[0]

            # get the md5 has of the canvas image
            canvas_image = data["canvas"]

            # decode the base64 string to bytes
            md5 = hashlib.md5(canvas_image.encode())
            canvas_image_md5 = md5.hexdigest()

            # add the row to the table row list
            table_rows.append([fingerprint_id,browser,mode,fingerprinting_mode,event,date,time,canvas_image,canvas_image_md5])

table_rows.sort(key=lambda x: (x[1], x[2], x[5]))

rows_html = ""
used_colors = {}
for row in table_rows:
    fingerprint_id, browser, mode, fingerprinting_mode, event, date, time, canvas_image, canvas_image_md5 = row
    color = "#000000"  # default color
    if canvas_image_md5 in used_colors:
        color = used_colors[canvas_image_md5]
    else:
        used_colors[canvas_image_md5] = get_random_color()
        color = used_colors[canvas_image_md5]
    row_html = f"""
        <tr>
            <td>{fingerprint_id}</td>
            <td>{browser}</td>
            <td>{mode}</td>
            <td>{fingerprinting_mode}</td>
            <td>{event}</td>
            <td>{date}</td>
            <td>{time}</td>
            <td><img src="{canvas_image}" style="max-height: 200px; max-width: 200px;"></td>
            <td><span style="color: {color};">{canvas_image_md5}</span></td>
        </tr>
    """
    rows_html += row_html

# build the complete HTML table
html_table = table_header + rows_html + table_footer

with open(f"{output_dir}/output.html", "w") as f:
    f.write(head)
    f.write(css_styles)
    f.write(head_end)
    f.write("<body>")
    f.write(html_table)
    f.write("</body>")
    f.write("</html>")



