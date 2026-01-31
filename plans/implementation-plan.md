# Implementation Plan

## Phase 1: Project Setup

### 1.1 Initialize Vite Project

```bash
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
```

### 1.2 Install Dependencies

```bash
# Core
npm install react-router-dom @tanstack/react-query zustand axios

# React Aria
npm install react-aria-components react-aria react-stately

# Styling
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npm install -D @tailwindcss/forms

# Icons
npm install @heroicons/react

# Utilities
npm install clsx tailwind-merge
```

### 1.3 Configuration Files

**tailwind.config.js**

- Configure content paths
- Add custom colors matching the dark theme
- Extend theme with animation utilities

**tsconfig.json**

- Path aliases for clean imports
- Strict type checking

**vite.config.ts**

- Path resolution
- Environment variables

---

## Phase 2: Core Infrastructure

### 2.1 API Types (`src/api/types.ts`)

```typescript
// Request types
interface ProcessRequest {
  chunk_size: number;
  overlap_size: number;
  Do_reset: number;
  file_id?: string;
}

interface SearchRequest {
  text: string;
  limit: number;
}

// Response types
interface HealthResponse {
  app_name: string;
  app_version: string;
}

interface UploadResponse {
  signal: string;
  file_id: string;
}

interface ProcessResponse {
  signal: string;
  Inserted_chunks: number;
  processed_files: number;
}

interface SearchResult {
  text: string;
  score: number;
  metadata?: Record<string, unknown>;
}

interface AnswerResponse {
  Signal: string;
  Answer: string;
  FullPrompt: string;
  ChatHistory: unknown[];
}
```

### 2.2 API Client (`src/api/client.ts`)

- Axios instance with base URL from settings
- Request/response interceptors
- Error handling

### 2.3 Store Setup (`src/stores/settingsStore.ts`)

- Persist settings to localStorage
- API URL configuration
- Project ID
- Theme preference
- Chat history

---

## Phase 3: UI Components

### 3.1 Layout Components

**MainLayout.tsx**

```
┌─────────────────────────────────────┐
│  Sidebar    │      Header          │
│             ├───────────────────────┤
│  - Logo     │                       │
│  - Nav      │      Page Content     │
│  - Project  │                       │
│  - Status   │                       │
│             │                       │
└─────────────────────────────────────┘
```

**Sidebar.tsx**

- Logo/brand
- Navigation links (Chat, Upload, Search, Index, Settings)
- Project selector (NumberField)
- API status indicator
- Quick links

**Header.tsx**

- Page title
- Theme toggle (Switch)
- Settings button

### 3.2 Base UI Components

**Button.tsx**

- Use React Aria Button
- Variants: primary, secondary, danger, ghost
- Sizes: sm, md, lg
- Loading state

**Card.tsx**

- Container with consistent styling
- Header, content, footer slots
- Hover effects

**Input.tsx**

- TextField wrapper
- Label, help text, error states
- Icons support

**FileDropzone.tsx**

- DropZone component
- Drag and drop visual feedback
- File type validation
- Multiple file support

**StatusBadge.tsx**

- Online/offline indicators
- Processing status
- Color-coded states

**MetricCard.tsx**

- Large metric display
- Title and value
- Trend indicators

---

## Phase 4: Page Implementations

### 4.1 ChatPage (`src/pages/ChatPage.tsx`)

**Layout:**

```
┌─────────────────────────────────────┐
│ Chat History (scrollable)           │
│ ┌─────────────────────────────────┐ │
│ │ User: Question...               │ │
│ └─────────────────────────────────┘ │
│ ┌─────────────────────────────────┐ │
│ │ AI: Answer...                   │ │
│ └─────────────────────────────────┘ │
├─────────────────────────────────────┤
│ Context: [────●────] 5 chunks       │
│ ┌─────────────────────────────────┐ │
│ │ Type message...         [Send]  │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

**Features:**

- Message list with auto-scroll
- Message types: user, assistant, system
- Input with keyboard shortcuts (Enter to send)
- Context limit slider (1-10)
- Loading state during API call
- Error handling with retry
- Chat history persistence

**Components:**

- ChatMessageList
- ChatMessageBubble
- ChatInput
- ContextLimitSlider

### 4.2 UploadPage (`src/pages/UploadPage.tsx`)

**Layout:**

```
┌─────────────────────────────────────┐
│ [Drop files here or click to browse]│
├─────────────────────────────────────┤
│ Uploaded Files:                     │
│ • file1.pdf (2.3 MB) ✓              │
│ • file2.txt (1.1 KB) ✓              │
├─────────────────────────────────────┤
│ Processing Configuration:           │
│ Chunk Size:    [_______] 512        │
│ Overlap:       [_______] 50         │
│ [ ] Reset existing chunks           │
│ [Process Files]                     │
├─────────────────────────────────────┤
│ Indexing:                           │
│ [ ] Reset existing index            │
│ [Push to Vector DB]                 │
└─────────────────────────────────────┘
```

**Features:**

- Drag and drop file upload
- Multiple file upload support
- File list with status
- Processing configuration
- Progress indicators
- Step-by-step workflow

**Components:**

- FileDropzone
- UploadedFileList
- ProcessConfigForm
- IndexButton

### 4.3 SearchPage (`src/pages/SearchPage.tsx`)

**Layout:**

```
┌─────────────────────────────────────┐
│ [Search query...            ] [🔍]  │
│ Results: [────●────] 5              │
├─────────────────────────────────────┤
│ Result #1 (Score: 0.89)      [▼]    │
│ Machine learning is a subset...     │
├─────────────────────────────────────┤
│ Result #2 (Score: 0.76)      [▶]    │
├─────────────────────────────────────┤
│ Result #3 (Score: 0.65)      [▶]    │
└─────────────────────────────────────┘
```

**Features:**

- Search input with enter key support
- Results limit slider (1-20)
- Expandable result cards
- Relevance scoring display
- Metadata viewer

**Components:**

- SearchInput
- ResultsLimitSlider
- SearchResultCard
- SearchResultList

### 4.4 IndexInfoPage (`src/pages/IndexInfoPage.tsx`)

**Layout:**

```
┌─────────────────────────────────────┐
│ [Refresh Index Info]                │
├─────────────────────────────────────┤
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│ │ Status  │ │ Vectors │ │ Project │ │
│ │ Active  │ │  1,234  │ │    1    │ │
│ └─────────┘ └─────────┘ └─────────┘ │
├─────────────────────────────────────┤
│ [View Full Response]         [▼]    │
│ {                                   │
│   "CollectionInfo": {               │
│     "vectors_count": 1234           │
│   }                                 │
│ }                                   │
└─────────────────────────────────────┘
```

**Features:**

- Metric cards for key stats
- Refresh button with loading state
- Expandable JSON viewer
- Auto-refresh option

**Components:**

- MetricCard
- RefreshButton
- JsonViewer

### 4.5 SettingsPage (`src/pages/SettingsPage.tsx`)

**Layout:**

```
┌─────────────────────────────────────┐
│ API Configuration                   │
│ Base URL: [http://localhost:8000/]  │
│                                     │
│ Project                             │
│ Project ID: [1]                     │
│                                     │
│ Appearance                          │
│ [●] Dark Mode                       │
│                                     │
│ Quick Links                         │
│ • Grafana • Prometheus • Qdrant     │
│   • API Docs                        │
└─────────────────────────────────────┘
```

**Features:**

- API URL input with validation
- Project ID selector
- Theme toggle
- Persistent settings
- Quick links to external tools

---

## Phase 5: Polish

### 5.1 Error Handling

- Toast notifications for errors
- Retry mechanisms
- Error boundaries
- Offline detection

### 5.2 Loading States

- Skeleton loaders
- Progress bars for long operations
- Button loading states
- Page transition animations

### 5.3 Responsive Design

- Mobile navigation (hamburger menu)
- Responsive grid layouts
- Touch-friendly controls
- Collapsible sidebar

### 5.4 Dark Mode

- CSS variables for theming
- System preference detection
- Manual toggle
- Persistent preference

---

## Phase 6: Build & Deploy

### 6.1 Build Configuration

- Production build optimization
- Environment variables
- Static asset handling

### 6.2 Docker Integration

- Multi-stage Dockerfile
- Nginx configuration for SPA
- Integration with existing Docker Compose

### 6.3 Documentation

- README with setup instructions
- Environment variable reference
- API integration guide

---

## File Checklist

### Required Files to Create:

**Config:**

- [ ] `frontend/package.json`
- [ ] `frontend/tsconfig.json`
- [ ] `frontend/vite.config.ts`
- [ ] `frontend/tailwind.config.js`
- [ ] `frontend/postcss.config.js`

**API:**

- [ ] `frontend/src/api/client.ts`
- [ ] `frontend/src/api/types.ts`
- [ ] `frontend/src/api/data.ts`
- [ ] `frontend/src/api/nlp.ts`
- [ ] `frontend/src/api/base.ts`

**Stores:**

- [ ] `frontend/src/stores/settingsStore.ts`

**Components - UI:**

- [ ] `frontend/src/components/ui/Button.tsx`
- [ ] `frontend/src/components/ui/Card.tsx`
- [ ] `frontend/src/components/ui/Input.tsx`
- [ ] `frontend/src/components/ui/FileDropzone.tsx`
- [ ] `frontend/src/components/ui/StatusBadge.tsx`
- [ ] `frontend/src/components/ui/MetricCard.tsx`
- [ ] `frontend/src/components/ui/Slider.tsx`

**Components - Layout:**

- [ ] `frontend/src/components/layout/Sidebar.tsx`
- [ ] `frontend/src/components/layout/Header.tsx`
- [ ] `frontend/src/components/layout/MainLayout.tsx`

**Components - Features:**

- [ ] `frontend/src/components/chat/ChatMessageList.tsx`
- [ ] `frontend/src/components/chat/ChatMessageBubble.tsx`
- [ ] `frontend/src/components/chat/ChatInput.tsx`
- [ ] `frontend/src/components/chat/ContextLimitSlider.tsx`
- [ ] `frontend/src/components/upload/UploadedFileList.tsx`
- [ ] `frontend/src/components/upload/ProcessConfigForm.tsx`
- [ ] `frontend/src/components/search/SearchResultCard.tsx`
- [ ] `frontend/src/components/search/SearchResultList.tsx`

**Pages:**

- [ ] `frontend/src/pages/ChatPage.tsx`
- [ ] `frontend/src/pages/UploadPage.tsx`
- [ ] `frontend/src/pages/SearchPage.tsx`
- [ ] `frontend/src/pages/IndexInfoPage.tsx`
- [ ] `frontend/src/pages/SettingsPage.tsx`

**Hooks:**

- [ ] `frontend/src/hooks/useApi.ts`
- [ ] `frontend/src/hooks/useSettings.ts`

**Utils:**

- [ ] `frontend/src/utils/helpers.ts`
- [ ] `frontend/src/utils/classNames.ts`

**Styles:**

- [ ] `frontend/src/index.css`
- [ ] `frontend/src/styles/theme.css`

**Root:**

- [ ] `frontend/src/main.tsx`
- [ ] `frontend/src/App.tsx`
- [ ] `frontend/index.html`
