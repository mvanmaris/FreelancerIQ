from project import calculate_minutes_per_unit, calculate_total_cost, calculate_cost_per_unit, load_data

def test_calculate_minutes_per_unit():
    assert calculate_minutes_per_unit(8, 40) == 12

def test_calculate_total_cost():
    assert calculate_total_cost(8, 40) == 320
    assert calculate_total_cost(5, 25) == 125

def test_calculate_cost_per_unit():
    assert calculate_cost_per_unit(320, 40) == 8
    assert calculate_cost_per_unit(125, 25) == 5
    assert calculate_cost_per_unit(320, 0) == None

def test_load_data():
    data = load_data("sample_data.csv")

    assert len(data) == 18
    assert data[0]["hours"] == 8
    assert data[0]["content_units"] == 45
    assert isinstance(data[0]["hours"], float)
    assert isinstance(data[0]["content_units"], int)
