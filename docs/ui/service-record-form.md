# Service record form

Opened from Vehicle detail. The vehicle summary (model, plate, last mileage) is shown at the top and cannot be changed.

- Workshop: shown read-only, taken from the mechanic's assignment.
- Date (default today), mileage (hint: "last recorded: 148,200 km"), labor cost in RSD, notes.
- Codes read: multiselect of codes, each with an optional note.
- Parts replaced: editable table (`st.data_editor`) with columns component, part number, brand, quantity, price per piece in RSD. Rows can be added and removed.
- Live totals under the table: parts, labor, total.
- Buttons: Save, Cancel.
- On error the form keeps the input and shows the message (for example mileage too low).
