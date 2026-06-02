from app import app


def test_header_present(dash_duo):
    dash_duo.start_server(app)

    header = dash_duo.find_element("#header")

    assert header.text == "Soul Foods Pink Morsel Sales Visualiser"


def test_graph_present(dash_duo):
    dash_duo.start_server(app)

    graph = dash_duo.find_element("#sales-graph")

    assert graph is not None


def test_region_picker_present(dash_duo):
    dash_duo.start_server(app)

    region_picker = dash_duo.find_element("#region-filter")

    assert region_picker is not None