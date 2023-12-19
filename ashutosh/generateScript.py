import json

def append_execfile_content():
    with open('selectedFileName.txt', 'r') as file:
        selected_names = file.readlines()

    with open('data.json', 'r') as file:
        data = json.load(file)

    with open('My-Script.sh', 'a') as my_script:
        for name in selected_names:
            name = name.strip()
            for key, value in data.items():
                if value['name'] == name:
                    with open(value['execFile'], 'r') as execfile:
                        content = execfile.read()
                        my_script.write(content)
                    break

append_execfile_content()