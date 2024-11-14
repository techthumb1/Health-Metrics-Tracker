import urllib.parse

# Define the chart configuration for QuickChart
chart_config = {
    "type": "line",
    "data": {
        "labels": ["Day 1", "Day 2", "Day 3"],  # Replace with dynamic labels if needed
        "datasets": [
            {
                "label": "Heart Rate",
                "data": [80, 85, 90]  # Replace with dynamic data if available
            }
        ]
    }
}

# Encode the chart configuration for URL usage
encoded_config = urllib.parse.quote(str(chart_config))
quickchart_url = f"https://quickchart.io/chart?c={encoded_config}"

# Read the current README content
with open("README.md", "r") as file:
    readme_content = file.read()

# Define the placeholder for the dynamic chart
placeholder_text = "![Dynamic Heart Rate Chart](https://quickchart.io/chart?c=%7B%22type%22%3A%22line%22%2C%22data%22%3A%7B%22labels%22%3A%5B%22Day%201%22%2C%22Day%202%22%2C%22Day%203%22%5D%2C%22datasets%22%3A%5B%7B%22label%22%3A%22Heart%20Rate%22%2C%22data%22%3A%5B80%2C85%2C90%5D%7D%5D%7D%7D)"

# Replace the placeholder with the updated QuickChart URL
updated_content = readme_content.replace(placeholder_text, f"![Dynamic Heart Rate Chart]({quickchart_url})")

# Write the updated content back to README.md
with open("README.md", "w") as file:
    file.write(updated_content)

print("README.md updated with the latest chart data.")
