# Phase 0 Tech Stack Summary: Photo Date-Album Organization

## Tech Stack Overview

### Frontend

| Category | Adopted Technology | Purpose |
| --- | --- | --- |
| Build tooling | `Vite` | Local development and frontend builds |
| UI technology | `HTML` / `CSS` / `JavaScript` | Page structure, styling, and interaction |
| Drag-and-drop interaction | `HTML Drag and Drop API` | Photo sorting within the same date album |

### Backend

| Category | Adopted Technology | Purpose |
| --- | --- | --- |
| Runtime environment | `Node.js` | Backend runtime environment |
| HTTP framework | `Express` | API routing and server handling |
| Upload handling | `multer` | Multi-file photo upload |

### Data & Media Handling

| Category | Adopted Technology | Purpose |
| --- | --- | --- |
| Database | `MySQL` | Stores albums, photos, and sorting data |
| ORM / Schema | `Prisma` | Schema, migrations, and data model access |
| EXIF parsing | `exifr` | Reads capture dates |
| Thumbnail handling | `sharp` | Generates thumbnails and processes images |

### Testing & Verification

| Category | Adopted Technology | Purpose |
| --- | --- | --- |
| Frontend BDD techstack | `Playwright` | webapp E2E, runs frontend Gherkin |
| Backend BDD techstack | `behave` | backend E2E, runs backend Gherkin, verifies API and authoritative state |

## Technologies Not Introduced in This Development

- `React` or other frontend frameworks
- Third-party drag-and-drop packages (e.g. `SortableJS`)
- Filesystem path-based image storage
