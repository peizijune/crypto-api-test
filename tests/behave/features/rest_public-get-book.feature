Feature: Public REST - get candlestick (data-driven)
  As an API consumer
  I want to retrieve candlestick data
  So that I can validate the exchange REST API is reachable

  Scenario Outline: Get <instrument_name> candlestick successfully
    Given I am using the "UAT" environment
    When I send GET "public/get-candlestick" with query:
      | instrument_name | <instrument_name> |
    Then the response status should be 200
    And the response should contain any of the keys:
      | result |
      | data   |

    Examples:
      | instrument_name |
      | BTCUSD-PERP     |

