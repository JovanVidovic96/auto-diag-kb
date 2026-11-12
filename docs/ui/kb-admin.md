# Knowledge base admin

- Type select: codes, symptoms, causes, solutions, makers, models, engines, components.
- Table of items of that type with search, and buttons New, Edit, Delete.
- Edit form with English and Serbian fields side by side. English is marked required.
- Links panel on the right for the selected item:
    - outgoing and incoming edges grouped by edge type, with their attributes
    - "Add link": edge type, target (searchable), attributes (weight, probability, priority, frequency, years depending on type)
    - delete per link
    - for codes, the current sum of `caused_by` probabilities, red when it would go over 1
- Delete asks for confirmation. If the item is used in service records, the API error is shown.
