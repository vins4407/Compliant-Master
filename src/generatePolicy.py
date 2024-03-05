import json

def generateJson(metric_list, data_file_path,output_file_path):
    with open(data_file_path, 'r') as data_file:
        data = json.load(data_file)

    policies = {}

    for metric in metric_list:
        for key, value in data.items():
            if value.get("name") == metric:
                # Exclude the "execFile" key
                value.pop("execFile", None)
                policies[key] = value

    # Write the result to a new JSON file
    with open(output_file_path, 'w') as output_file:
        json.dump(policies, output_file, indent=2)




# Example usage: Fetch data for the given metrics and save it to output.json
