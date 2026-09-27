Feature: {{FEATURE_TITLE}}

  # By default start directly from Rule / Example; do not treat Background as the opening move.
  # Only when multiple Examples truly share the same steps with test semantics, and extracting is more readable, add a Background.
  # Do not write spec summaries, worldview, or global rule primers as Background.

  Rule: {{RULE_NAME}}

    # [need clarification] {{CLARIFICATION_QUESTION_1}}

    Example: {{JOURNEY_EXAMPLE_TITLE}}
      Given {{ACTOR_NAME}} already has {{PRECONDITION_SUMMARY}}
      And the scenario for {{ACTOR_NAME}} is as follows:
        | {{SETUP_TABLE_HEADER_1}} | {{SETUP_TABLE_HEADER_2}} | {{SETUP_TABLE_HEADER_3}} |
        | {{SETUP_TABLE_VALUE_1}}  | {{SETUP_TABLE_VALUE_2}}  | {{SETUP_TABLE_VALUE_3}}  |
      When {{ACTOR_NAME}} {{PRIMARY_ACTION}}
      And {{ACTOR_NAME}} {{SECONDARY_ACTION}}
      Then {{PRIMARY_BUSINESS_OUTCOME}}
      And {{SUMMARY_LABEL}} is as follows:
        | Item               | Value               |
        | {{SUMMARY_ITEM_1}} | {{SUMMARY_VALUE_1}} |
        | {{SUMMARY_ITEM_2}} | {{SUMMARY_VALUE_2}} |
      And {{FOLLOW_UP_OUTCOME}}
