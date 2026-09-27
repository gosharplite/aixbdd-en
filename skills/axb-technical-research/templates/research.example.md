# Phase 0 Research: Photo Date-Album Organization

## Decision 1: Adopt a minimal front-back separated Web architecture

- **Decision**: Adopt the `frontend/` `Vite + native HTML/CSS/JS` and `backend/` `Node.js + Express` separated architecture.
- **Rationale**: This architecture best fits the requirements of "teaching-friendly, few packages, directly connecting to the photo upload API", and clearly separates UI, HTTP, and data persistence responsibilities.
- **Alternatives considered**:
  - Monolithic SSR: the initial version needs no server-side template rendering; it would increase page coupling.
  - React SPA: exceeds the user's request and increases conceptual and dependency complexity.

## Decision 2: The frontend keeps only Vite as its core tool

- **Decision**: The frontend runtime uses only `vite`; everything else — state management, data fetching, and image display — is implemented with native browser capabilities.
- **Rationale**: The homepage requirements concentrate on list rendering, drag-and-drop sorting, upload, and state switching; native ES modules suffice; avoiding extra frameworks reduces bundle size, learning cost, and debugging surface.
- **Alternatives considered**:
  - Introducing a state management library: insufficient value for a small single-page app.
  - Introducing a UI component library: would weaken the native foundation of the teaching demonstration.

## Decision 3: Drag-and-drop sorting adopts the browser-native Drag and Drop

- **Decision**: Photo reordering within the same date album preferentially uses the native `HTML Drag and Drop API`; no third-party drag-and-drop package is introduced.
- **Rationale**: The requirement only covers "reorder within the same album; no cross-album moves"; the interaction model is simple; the native API suffices and makes DOM and sorting logic easier to explain in a course.
- **Alternatives considered**:
  - `SortableJS`: convenient, but an extra dependency for this case that obscures the core sorting rules.
  - Fully custom with `Pointer Events`: highly flexible, but cost exceeds the requirement for the initial version.

## Decision 4: The backend adopts an ORM to manage MySQL and the data model

- **Decision**: The backend uses `express`, `multer`, `@prisma/client`, `exifr`, `sharp` as core runtime packages, with `prisma` managing schema and migrations.
- **Rationale**:
  - `express`: a minimal and mature HTTP API framework
  - `multer`: simplifies `multipart/form-data` multi-file upload
  - `Prisma ORM`: manages data structures with type-safe models, migrations, and relations — friendlier for teaching and later maintenance
  - `exifr`: parses photo capture dates
  - `sharp`: generates thumbnails, reducing homepage load cost
- **Alternatives considered**:
  - `mysql2` writing SQL directly: fewer dependencies, but worse schema evolution, relation management, and teaching readability
  - `Knex`: closer to SQL, but less direct than Prisma in model expression and type integration

## Decision 5: Originals and thumbnails are stored directly in MySQL BLOB

- **Decision**: Both originals and thumbnails are stored in MySQL `BLOB/LONGBLOB` fields, and the backend API streams preview content directly to the frontend.
- **Rationale**: This brings photo contents and metadata into the same transaction boundary and backup scope, is more intuitive for teaching demonstrations, and avoids separately managing filesystem paths and cleanup issues.
- **Alternatives considered**:
  - Filesystem paths + DB metadata: saves database capacity, but adds path synchronization and deletion consistency issues
  - Cloud object storage: better extensibility, but exceeds the initial teaching goal

## Decision 6: Date grouping is EXIF-first, with the import date as the last fallback

- **Decision**: Prefer reading EXIF `DateTimeOriginal`, then other EXIF/file times; if none are available, use the import day's date as `album_date`.
- **Rationale**: This fully aligns with the spec's clarified answers and guarantees every photo lands in a browsable date album.
- **Alternatives considered**:
  - Collecting undated photos into an "unknown date" album: violates the clarified requirement
  - Using only file creation time: easily mismatches the real capture date

## Decision 7: Photo previews stream thumbnail BLOBs via a backend image endpoint

- **Decision**: `GET /api/albums` and `GET /api/albums/{id}/photos` return only the metadata needed for previews plus `previewUrl`; `previewUrl` streams the thumbnail `BLOB` from the database via a backend image endpoint.
- **Rationale**: The requirement demands up to 200 visible photos remain browsable within 2 seconds, so even with images in the database, the smaller thumbnail content must be transmitted first — not the originals.
- **Alternatives considered**:
  - Frontend scaling originals itself: wastes bandwidth and causes rendering pressure
  - Showing only filenames without thumbnails: fails the tiled-preview requirement

## Decision 8: Sorting persistence adopts an in-album `sort_key`

- **Decision**: Keep `sort_key` and `sort_mode` on `photos` records, defaulting to capture-time order; switch to manual ordering after a successful drag-and-drop.
- **Rationale**: This satisfies "updates immediately and remains consistent after re-entry" without adding a separate sorting table.
- **Alternatives considered**:
  - Rewriting the whole album's sequential numbers on every drop: feasible, but higher update cost
  - Creating a separate sorting table: over-engineered for the MVP

## Decision 9: BDD techstack is designated per end

- **Decision**: The frontend webapp's Gherkin lands with `Playwright`; the backend API's Gherkin lands with `behave`.
- **Rationale**: This is the AIxBDD workflow — the BDD techstack must be clarified first. The frontend verifies screen operations; the backend verifies API and authoritative state; the runners cannot be merged into one.
- **Alternatives considered**:
  - Playwright for both frontend and backend: backend authoritative state should not be inferred from screens alone.
  - behave for both frontend and backend: behave is not the default for frontend webapp E2E.

## Decision 10: The test strategy defaults to E2E everywhere

- **Decision**: The frontend uses Playwright for webapp E2E; the backend uses behave to hit the API and database authoritative state. Import grouping, album queries, sorting persistence, and cross-album rejection all go through E2E; the main acceptance is not shrunk into unit tests or manual Quickstart.
- **Rationale**: When the test strategy is not changed, the default is E2E everywhere. Whether drag-and-drop and the list really update must be seen on screen; grouping and rejection must be seen in the backend authoritative state.
- **Alternatives considered**:
  - `vitest + supertest` first, E2E later: would test the acceptance journey into fake greens.
  - No automation at all: Gherkin would have no landing.
