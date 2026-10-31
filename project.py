import csv
import io

def main():
    data = load_data("sample_data.csv")

    for row in data:
        minutes_per_unit = calculate_minutes_per_unit(row["hours"], row["content_units"])
        total_cost = calculate_total_cost(row["hours"], row["hourly_rate"])
        cost_per_unit = calculate_cost_per_unit(total_cost, row["content_units"])

        # cformat reluts and handle zero content units
        if minutes_per_unit is None:
            minutes_display = "N/A"
        else:
            minutes_display = f"{minutes_per_unit:.2f}"

        if cost_per_unit is None:
            cost_display = "N/A"
        else:
            cost_display = f"${cost_per_unit:.2f}"
        print(
            f"{row['freelancer']}: "
            f"{minutes_display} min/unit | "
            f"Total Cost: ${total_cost:.2f} | "
            f"Cost/unit: {cost_display}"
        )

# calculate minutes per unit
def calculate_minutes_per_unit(hours, content_units):
    if content_units == 0:
        return None

    return (hours * 60) / content_units

# calculate total cost
def calculate_total_cost(hours, hourly_rate):
    return hours * hourly_rate

# calculate cost per unit
def calculate_cost_per_unit(total_cost, content_units):
    if content_units == 0:
        return None

    return total_cost / content_units

# load csv file
def load_data(filename):
    rows = []

    if isinstance(filename, str):
        file = open(filename, newline="")
    else:
        file = io.StringIO(filename.getvalue().decode("utf-8-sig"))

    with file:
        reader = csv.DictReader(file)

        # convert csv values into numbers
        for row in reader:
            row["content_units"] = int(row["content_units"])
            row["hours"] = float(row["hours"])
            row["hourly_rate"] = float(row["hourly_rate"])
            rows.append(row)

    return rows








if __name__ == "__main__":
    main()
