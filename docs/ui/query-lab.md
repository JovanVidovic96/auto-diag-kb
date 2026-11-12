# Query Lab

Built for the defense.

- Left: list of queries Q1 to Q18 with their one-line question and the course requirement they show.
- Right, for the selected query:
    - AQL text with syntax highlighting
    - form for bind variables, prefilled with an example that returns data
    - buttons Run, Explain, Profile
    - Run: result as a table, or as JSON for nested results
    - Explain: list of plan nodes (type, estimated cost), indexes used, and a warning line when an `EnumerateCollectionNode` scans a collection that has an index
    - Profile: execution time, documents scanned full and by index, peak memory
- "Compare" toggle for indexed queries: runs the query normally and again with the optimizer rule `use-indexes` turned off (`optimizer_rules=["-use-indexes"]` in python-arango), then shows both plans and both stats side by side. This shows the effect of an index without dropping it.
