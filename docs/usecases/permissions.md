# Permissions

| Action | Guest | Owner | Mechanic | Admin |
| --- | --- | --- | --- | --- |
| Register, log in | yes | | | |
| Read knowledge base and catalog | | yes | yes | yes |
| Diagnose, search, nearest workshop | | yes | yes | yes |
| Create, edit, delete knowledge base items and links | | | | yes |
| Create, edit, delete catalog (makers, models, engines, components) | | | | yes |
| Register a vehicle | | yes (for self) | | yes (for anyone) |
| List vehicles | | own only | all | all |
| View vehicle history | | own only | all | all |
| Transfer a vehicle | | own only | | yes |
| Create service record | | | yes | |
| Edit or delete service record | | | own records | all |
| View analytics | | | yes | yes |
| Query Lab | | | | yes |
| Manage users, roles, workshops, mechanic assignment | | | | yes |

"Own" for a vehicle means an `owns` edge from the user with `until == null`. "Own" for a service record means a `performed_by` edge pointing to the mechanic.

A mechanic who is not assigned to a workshop (no `works_at` edge) cannot create service records and gets `409` with a message to ask an admin.

Only mechanics create service records, because every record needs the workshop from `works_at`. Admin corrects or deletes records but does not enter new ones.
