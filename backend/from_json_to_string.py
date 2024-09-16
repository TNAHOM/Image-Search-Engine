def convert_json_to_string(json_data):
    description = json_data.get("description", [])
    if not description:
        return "No description available."

    item = description[0]
    output_parts = []

    for key, value in item.items():
        if key == "other":
            if value:
                output_parts.append(f"other is {value}")
        else:
            formatted_key = key.lower().replace("_", " ")
            if isinstance(value, list):
                output_parts.append(f"{formatted_key} is {', '.join(value)}")
            else:
                output_parts.append(f"{formatted_key} is {value}")

    return ", ".join(output_parts)
