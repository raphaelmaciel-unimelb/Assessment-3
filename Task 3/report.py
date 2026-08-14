# ----------------------
# Assessment 3 - Task 3
# Utility functions for generating the weather report in HTML.
# Student: Raphael Barbosa Maciel
# Subject: AI Programming Fundamentals (COMP90100_2026_OT4_UMO_1)
# GitHub repo: https://github.com/raphaelmaciel-unimelb/Assessment-3
# ---------------------

try:
    from datetime import datetime, timezone, UTC
    from zoneinfo import ZoneInfo
    import weather as weather
    import collector as collector
    import WMO_code as code
    import json
    from jinja2 import Template

    from dotenv import load_dotenv

    load_dotenv()

except (SyntaxError, ImportError, NameError) as synt_err:
     print(f"  [warn] Environment is not ready or Import has failed: {synt_err}")

except Exception as e:
     print(f"  [warn] Environment is not ready or Import has failed: {e}")


def read_log(log_path):
    """Read weather records from a JSON log file.

    Args:
        log_path: Path to the JSON file containing saved weather records.

    Returns:
        A list of weather record dictionaries. If the file does not exist or
        contains invalid JSON, an empty list is returned.
    """
    list_results=[]

    try:
        # Load the JSON weather log so the summary can be rebuilt from stored records.
        with open(log_path, "r", encoding="utf-8") as file:
                    content = file.read().strip()
                    if content:
                        json_content = json.loads(content)
                        if isinstance(json_content, list):
                            list_results = json_content

    except (AttributeError, FileNotFoundError, json.decoder.JSONDecodeError) as file_not_found:
        print(f"   [Error] read_log() file error: {file_not_found}")
        return []

    return list_results


def generate_report(log_path, output_path):
    """Generate an HTML weather report from a saved weather log.

    The function reads the log, summarises the data, converts timestamps to
    Melbourne time, and writes the rendered report to the output HTML file.

    Args:
        log_path: Path to the JSON weather log.
        output_path: Path where the generated HTML report should be saved.
    """

    # Read the log entries from the JSON file.
    log_records_list = read_log(log_path)

    # Retrieve the weather summary from the collector module.
    summary = collector.summarise_log(log_path)
    
    data_list=[] 
    dates = []
    
    # Iterate through the log records and prepare the data for the table.
    for record in log_records_list:
        code_description = code.get_code_description(record["weather"]["weathercode"])
        date_convertion = datetime.fromisoformat(record.get('fetched_at')).astimezone(ZoneInfo("Australia/Melbourne"))
        
        data={
            "city":record.get('city'),
            "timestamp":date_convertion,
            "temperature (°C)":record["weather"]["temperature"],
            "windspeed (km/h)":record["weather"]["windspeed"],
            "weathercode description":code_description
        }

        dates.append(record.get('fetched_at'))        
        data_list.append(data)
    
    # Get the current time for the report heading timestamp.
    timestamp_now = datetime.now(ZoneInfo("Australia/Melbourne"))

    # Get the earliest record for the date range field.
    date_from = min(
        dates,
        key=lambda d: datetime.fromisoformat(d).astimezone(timezone.utc)
    )
    date_from = datetime.fromisoformat(date_from).astimezone(ZoneInfo("Australia/Melbourne"))

    # Get the latest record for the date range field.
    date_to = max(
        dates,
        key=lambda d: datetime.fromisoformat(d).astimezone(timezone.utc)
    )
    date_to = datetime.fromisoformat(date_to).astimezone(ZoneInfo("Australia/Melbourne"))

    # Extract the table headers from the first data dictionary.
    log_entries_table_header = list(data_list[0].keys())

    # Sort the log entries by timestamp.
    data_list = sorted(data_list, key=lambda item: item['timestamp'])
    
    html_style= """            
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 40px;
                    background-color: #f8f9fa;
                    color: #333;
                }
                h1 {
                    color: #2c3e50;
                    margin-bottom: 20px;
                }
                .styled-table {
                    border-collapse: collapse;
                    width: 100%;
                    background: #fff;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    border-radius: 8px;
                    overflow: hidden;
                }
                .styled-table th {
                    background-color: #34495e;
                    color: #ffffff;
                    text-align: left;
                    padding: 12px 15px;
                    font-weight: 600;
                }
                .styled-table td {
                    padding: 12px 15px;
                    border-bottom: 1px solid #dddddd;
                }
                .styled-table tbody tr:nth-of-type(even) {
                    background-color: #f3f3f3;
                }
                .styled-table tbody tr:last-of-type {
                    border-bottom: 2px solid #34495e;
                }
            </style>
        """
    
    html_header="""
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Weather Report A3.Task3</title>
            <timestamp>{{ timestamp_now.strftime('%d-%m-%Y %H:%M:%S') }}</timestamp>
            {{html_style}}
        </head>
        """
    html_body="""
        <body>
                <h1>Weather Report</h1>
                <p> <b>Subject:</b> AI Programming Fundamentals (COMP90100_2026_OT4_UMO_1)</p>
                <p> <b>Student:</b> Raphael Barbosa Maciel</p>
                <p> <b>GitHub repo:</b> <a href=https://github.com/raphaelmaciel-unimelb/Assessment-3>https://github.com/raphaelmaciel-unimelb/Assessment-3</a></p>
                <h2>Summary</h2>
                <table class="styled-table">
                    <thead>
                        <tr>
                            <th>Data</th>
                            <th>Value</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Total records</td>
                            <td>{{ summary["total_records"] }}</td>
                        </tr>
                        <tr>
                            <td>Cities tracked</td>
                            <td>
                                {% for city in summary["cities_tracked"] %}
                                    {{ city }}{% if loop.nextitem %}, {% endif %}
                                {% endfor %}
                            </td>
                        </tr>
                        <tr>
                            <td>Date from</td>
                            <td>{{ date_from.strftime('%d-%m-%Y %H:%M:%S') }}</td>
                        </tr>
                        <tr>
                            <td>Date to</td>
                            <td>{{ date_to.strftime('%d-%m-%Y %H:%M:%S') }}</td>
                        </tr>
                    </tbody>
                </table>
                <h2>Log entries</h2>
                <table class="styled-table">
                    <thead>
                        <tr>
                            {# Dynamic header generation loop #}
                            {% for entry in entries_table_header %}
                                <th>{{ entry.title() }}</th>
                            {% endfor %}
                        </tr>
                    </thead>
                    <tbody>
                        {# Dynamic row generation loop #}
                        {% for row in data_list %}
                        <tr>
                            {% for entry in entries_table_header %}
                                {% if entry == 'timestamp' %}
                                    <td>{{ row[entry].strftime('%d-%m-%Y %H:%M:%S') }}</td>
                                {% else %}
                                    <td>{{ row[entry] }}</td>
                                {% endif %}

                            {% endfor %}
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
    
        </body>
        """
    
    # Build the HTML structure with embedded CSS.
    html_template_string = f"""<!DOCTYPE html>
        <html lang="en">
            {html_header}
            {html_body}
        </html>
        """

    # Render the HTML using the Jinja2 template engine.
    template = Template(html_template_string)

    # Render the HTML and save it to the output file.
    rendered_html = template.render(
        timestamp_now=timestamp_now,
        html_style=html_style,
        summary=summary,
        date_from=date_from,
        date_to=date_to,
        entries_table_header=log_entries_table_header,
        data_list=data_list
    )

    # Write the rendered HTML to the output file.
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(rendered_html)
    

def main():
    """Generate the weather report for the saved log data.

    This function runs the data collection step and then writes the final
    HTML summary report to the output file.
    """
    collector.main()
    generate_report("weather_log.json", "weather_report.html")


if __name__ == "__main__":
    main()
    
    