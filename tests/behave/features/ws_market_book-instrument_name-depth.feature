Feature: WebSocket - subscribe to book channel (data-driven)
  As an API consumer
  I want to subscribe to a book channel
  So that I can validate the exchange WebSocket API is reachable

  Scenario Outline: Subscribe to <instrument_name> book channel with depth <depth>
    Given I am using the "UAT" environment
    When I connect to the market WebSocket
    And I subscribe to the "<instrument_name>" book channel with depth "<depth>"
    Then I should receive a message acknowledging subscription or data

    Examples:
      | instrument_name | depth |
      | BTCUSD-PERP     | 10    |
      | BTCUSD-PERP     | 50    |

