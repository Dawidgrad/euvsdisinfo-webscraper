import json

def save_to_json(data):
    with open('source/output/output_data.json', 'w', encoding='iso-8859-1') as f:
        json.dump(data, f)