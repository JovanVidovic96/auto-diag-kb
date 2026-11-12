# UI overview

The UI is a Streamlit multipage app. These pages describe what each screen contains; the drawings are added later.

## Common layout

- Sidebar: app name, EN / SR switch, the pages the current role can open, logged-in user and role, Log out.
- Main area: page title, then the content.
- Errors from the API are shown with `st.error` and the `detail` text. Validation errors are shown next to the field.
- All API calls go through `api_client.py`, which adds the token and `lang`.

## Pages by role

| Page | Guest | Owner | Mechanic | Admin |
| --- | --- | --- | --- | --- |
| [Login](login.md) | yes | | | |
| [Register](register.md) | yes | | | |
| [Diagnose](diagnose.md) | | yes | yes | yes |
| [Code lookup](code-lookup.md) | | yes | yes | yes |
| [Catalog](catalog.md) | | yes | yes | yes |
| [My vehicles](my-vehicles.md) | | yes | search mode | search mode |
| [Vehicle detail](vehicle-detail.md) | | own | yes | yes |
| [Service record form](service-record-form.md) | | | yes | edit only |
| [Analytics](analytics.md) | | | yes | yes |
| [Knowledge base admin](kb-admin.md) | | | | yes |
| [Users and workshops](users-admin.md) | | | | yes |
| [Query Lab](query-lab.md) | | | | yes |
