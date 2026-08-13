# ----------------------
# Assessment 3 - Task 3
# Utility functions for generating the weather report in HTML.
# Student: Raphael Barbosa Maciel
# Subject: AI Programming Fundamentals (COMP90100_2026_OT4_UMO_1)
# ---------------------

try:
    from datetime import datetime, UTC
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
        print(f"   [Error] summarise_log() File error: {file_not_found}")
        return []
    
    return list_results

def generate_report(log_path, output_path):

    log_records_list = read_log(log_path)

    summary = collector.summarise_log(log_path)
    
    data_list=[] 
    
    for record in log_records_list:
        code_description = code.get_code_description(record["weather"]["weathercode"])
        data={
            "city":record.get('city'),
            "timestamp":record.get('fetched_at'),
            "temperature (°C)":record["weather"]["temperature"],
            "windspeed (km/h)":record["weather"]["windspeed"],
            "weathercode description":code_description
        }
        data_list.append(data)
    
    # 1. Automatically extract table headers from the first data dictionary keys
    log_entries_table_headers = list(data_list[0].keys())
    
    html_header= """
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Weather Report A3.Task3</title>
            <timestamp>{{timestamp}}</timestamp>
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
        </head>
        """
    html_body="""
        <body>
                <h1>Weather app</h1>
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
                            <td>{{ summary["cities_tracked"] }}</td>
                        </tr>
                        <tr>
                            <td>Date range</td>
                            <td>{{ summary["latest_fetch"] }}</td>
                        </tr>                                                                
                    </tbody>
                </table>
                <h2>Log entries</h2>
                <table class="styled-table">
                    <thead>
                        <tr>
                            {# Dynamic Header Generation Loop #}
                            {% for header in headers %}
                            <th>{{ header.title() }}</th>
                            {% endfor %}
                        </tr>
                    </thead>
                    <tbody>
                        {# Dynamic Row Generation Loop #}
                        {% for row in data_list %}
                        <tr>
                            {% for header in headers %}
                            <td>{{ row[header] }}</td>
                            {% endfor %}
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
    
        </body>
        """
    
    # 2. Define the self-contained HTML structural template with embedded CSS
    html_template_string = f"""<!DOCTYPE html>
        <html lang="en">
            {html_header}
            {html_body}
        </html>
        """

    # 3. Process the data using the template engine
    template = Template(html_template_string)
    
    rendered_html = template.render(
        summary=summary, 
        headers=log_entries_table_headers, 
        data_list=data_list, 
        timestamp=collector.fetched_at()
        )
    
    # Render to string and save
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(rendered_html)
    

def main():
    collector.main()
    generate_report("weather_log.json", "weather_report.html")
    

if __name__ == "__main__":
    main()
    
    