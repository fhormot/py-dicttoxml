import pytest
# import xmltodict

from src.dicttoxml import dicttoxml

from pprint import pprint

@pytest.fixture
def fixture():
    yield dicttoxml()

def test_single_level_single_tag(fixture):
    dict = {
            "name": "test"
    }

    expected_output = [
        '<name>test</name>'
    ]

    result = fixture.xml(dict)
    assert result == expected_output

def test_single_level_multi_tag(fixture):
    dict = {
            "name": "test",
            "test": "test"
    }

    expected_output = [
        '<name>test</name>',
        '<test>test</test>'
    ]

    result = fixture.xml(dict)
    assert result == expected_output

def test_multi_level_single_tag(fixture):
    dict = {
            "test": {
                "test": "test"
            }
    }

    expected_output = [
        '<test>',
        '\t<test>test</test>',
        '</test>',
    ]

    result = fixture.xml(dict)

    assert result == expected_output

def test_multi_level_multi_tag(fixture):
    dict = {
            "test": {
                "test": "test",
                "test2": "test"
            }
    }

    expected_output = [
        '<test>',
        '\t<test>test</test>',
        '\t<test2>test</test2>',
        '</test>',
    ]

    result = fixture.xml(dict)

    assert result == expected_output

def test_none_in_field(fixture):
    dict = {
            "test": {
                "test": "test",
                "test2": None
            }
    }

    expected_output = [
        '<test>',
        '\t<test>test</test>',
        '\t<test2></test2>',
        '</test>',
    ]

    result = fixture.xml(dict)

    assert result == expected_output

def test_text_in_field(fixture):
    dict = {
            "test": {
                "#text": "text",
                "test2": "test"
            }
    }

    expected_output = [
        '<test>text',
        '\t<test2>test</test2>',
        '</test>',
    ]

    result = fixture.xml(dict)

    assert result == expected_output

def test_attribute_in_field(fixture):
    dict = {
            "test": {
                "@version": "7",
                "test2": "test"
            }
    }

    expected_output = [
        '<test version="7">',
        '\t<test2>test</test2>',
        '</test>',
    ]

    result = fixture.xml(dict)

    assert result == expected_output

    dict = {
            "test": {
                "@version": "7",
                "@other": "other",
                "test2": "test"
            }
    }

    expected_output = [
        '<test version="7" other="other">',
        '\t<test2>test</test2>',
        '</test>',
    ]

    result = fixture.xml(dict)

    assert result == expected_output

def test_attribute_and_text_in_field(fixture):
    dict = {
            "test": {
                "@version": "7",
                "#text": "text",
                "test2": "test"
            }
    }

    expected_output = [
        '<test version="7">text',
        '\t<test2>test</test2>',
        '</test>',
    ]

    result = fixture.xml(dict)

    assert result == expected_output

    dict = {
            "test": {
                "@version": "7",
                "#text": "text"
            }
    }

    expected_output = [
        '<test version="7">text</test>',
    ]

    result = fixture.xml(dict)

    assert result == expected_output

    print('\n')
    print(result)