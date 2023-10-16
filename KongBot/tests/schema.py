from bot.exploration import EXPAND_SECTION_SCHEMA

from .utils import validate_schema

import pytest

def test_schema_validate_pass():
    # The JSON data you want to validate
    json_data_to_validate = {
        "key": "\ndescribe funda_expansionHistorical Stru",
        "node": [
            {
                "expansion": "Notable Campaigns",
                "section": "The Women's Suffrage Movement in Canada was marked...",
                "keywords": [
                    "Women's Suffrage Movement in Canada",
                    "Ontario Mock Parliament",
                    "Winnipeg Women's Conference",
                    "campaigns"
                ]
            },
            # Add more objects to validate here if needed
        ]
    }

    assert validate_schema(json_data_to_validate, EXPAND_SECTION_SCHEMA)


def test_schema_validate_fail():
    # The JSON data you want to validate
    json_data_to_validate = {
        "key": "\ndescribe funda_expansionHistorical Stru",
        "node": [
            {
                "expansion": "Notable Campaigns",
                "section": [
                    {
                        "subsection":"The Women's Suffrage Movement in Canada was marked..."
                    }],
                "keywords": [
                    "Women's Suffrage Movement in Canada",
                    "Ontario Mock Parliament",
                    "Winnipeg Women's Conference",
                    "campaigns"
                ]
            },
            # Add more objects to validate here if needed
        ]
    }

    assert not validate_schema(json_data_to_validate, EXPAND_SECTION_SCHEMA)

def test_schema_validate_none_fail():
    # The JSON data you want to validate
    json_data_to_validate = None

    assert not validate_schema(json_data_to_validate, EXPAND_SECTION_SCHEMA)


if __name__ == "__main__":
    pytest.main()
