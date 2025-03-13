import pytest
import xmltodict
from pathlib import Path

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

def test_multi_level_single_tag_array(fixture):
    dict = {
            "top": [{
                "test": "test"
            },{
                "test": "test"
            },]
    }

    expected_output = [
        '<top>',
        '\t<test>test</test>',
        '</top>',
        '<top>',
        '\t<test>test</test>',
        '</top>',
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

def test_attributes_in_field(fixture):
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

def test_multi_level(fixture):
    dict = {
        "top": {
            "test": {
                "test2": "test"
            }
        }
    }

    expected_output = [
        '<top>',
        '\t<test>',
        '\t\t<test2>test</test2>',
        '\t</test>',
        '</top>',
    ]

    result = fixture.xml(dict)

    assert result == expected_output

def test_multi_level_array(fixture):
    dict = {
        "top": {
            "test": [
                {
                    "test2": "test"
                },
                {
                    "test2": "test"
                },]
        }
    }

    expected_output = [
        '<top>',
        '\t<test>',
        '\t\t<test2>test</test2>',
        '\t</test>',
        '\t<test>',
        '\t\t<test2>test</test2>',
        '\t</test>',
        '</top>',
    ]

    result = fixture.xml(dict)

    assert result == expected_output

def test_multi_level_xmltodict(fixture):
    expected_output = [
        '<outputs>',
        '\t<output>iltr_ip_tb_tb_iltr_redge_25n.t_delay_L2H',
        '\t\t<value>DSDP-REQ-660</value>',
        '\t\t<testname>iltr_ip_tb_tb_iltr_redge_25n</testname>',
        '\t\t<resname>t_delay_L2H</resname>',
        '\t</output>',
        '\t<output>iltr_ip_tb_tb_iltr_redge_25n.t_delay_H2L',
        '\t\t<value>DSDP-REQ-661</value>',
        '\t\t<testname>iltr_ip_tb_tb_iltr_redge_25n</testname>',
        '\t\t<resname>t_delay_H2L</resname>',
        '\t</output>',
        '</outputs>',
    ]

    dict = xmltodict.parse('\n'.join(expected_output))

    result = fixture.xml(dict)

    assert result == expected_output

# @pytest.mark.skip
def test_return_xml_w_file(fixture):
    path = Path('./tests/testfiles/maestro.sdb')

    with open(path, 'r', encoding='utf-8') as file:
        xml = file.read()

    file = xmltodict.parse(xml)

    result = fixture.return_xml(file)
    assert xml == result

    # path = Path('./tests/testfiles/maestro_result.sdb')
    # with open(path, 'w', encoding='utf-8') as file:
    #     file.write(result)