# Diagnose

The main page of the app. Two columns on desktop.

**Left column: input**

- Multiselect "What do you notice?" with all symptoms, searchable, grouped by system.
- Optional vehicle select. Owners get a dropdown of their vehicles; mechanics get a VIN or plate search box.
- Button: Diagnose.

**Right column: results**

- List of ranked codes. Each row: code, description, severity badge (1 to 5, color from green to red), a bar "3 of 4 symptoms", score.
- Clicking a row expands it:
    - causes sorted by probability, each with a probability bar
    - affected components under each cause
    - solutions in priority order with cost range in RSD and time in hours
    - button "Show graph", which opens an interactive graph of the code and its neighbors (pyvis)
- Empty state: "No code matches all selected symptoms. Try fewer symptoms or remove the vehicle."
