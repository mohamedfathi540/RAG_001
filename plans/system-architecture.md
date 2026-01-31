# System Architecture

## High-Level Architecture

```mermaid
flowchart TB
    subgraph Frontend["React SPA (New)"]
        UI[React Aria Components]
        Router[React Router]
        Query[TanStack Query]
        Store[Zustand Store]
        API[API Client]

        UI --> Router
        Router --> Query
        Query --> API
        Store --> UI
    end

    subgraph Backend["FastAPI Backend"]
        Routes[API Routes]
        Controllers[Controllers]
        Models[Models]
        VectorDB[(Vector DB)]

        Routes --> Controllers
        Controllers --> Models
        Models --> VectorDB
    end

    subgraph External["External Services"]
        LLM[LLM Providers]
        Embeddings[Embedding Service]
    end

    API --> Routes
    Controllers --> LLM
    Controllers --> Embeddings
```

## Component Hierarchy

```mermaid
flowchart TD
    App[App]

    App --> Router[BrowserRouter]
    Router --> Layout[MainLayout]

    Layout --> Sidebar[Sidebar]
    Layout --> Header[Header]
    Layout --> Content[Page Content]

    Sidebar --> Nav[Navigation Links]
    Sidebar --> ProjectSelect[Project Selector]
    Sidebar --> ApiStatus[API Status]

    Header --> ThemeToggle[Theme Toggle]
    Header --> SettingsBtn[Settings Button]

    Content --> Routes[Routes]

    Routes --> Chat[ChatPage]
    Routes --> Upload[UploadPage]
    Routes --> Search[SearchPage]
    Routes --> Index[IndexInfoPage]
    Routes --> Settings[SettingsPage]

    Chat --> ChatList[ChatMessageList]
    Chat --> ChatInput[ChatInput]
    Chat --> ContextSlider[ContextLimit Slider]

    Upload --> FileDrop[FileDropzone]
    Upload --> FileList[UploadedFileList]
    Upload --> ProcessForm[ProcessConfig Form]
    Upload --> IndexBtn[IndexButton]

    Search --> SearchInput[SearchInput]
    Search --> ResultsList[SearchResults]
    Search --> LimitSlider[ResultsLimit Slider]

    Index --> Metrics[MetricsCards]
    Index --> RefreshBtn[RefreshButton]
    Index --> JsonView[JSON Viewer]
```

## Data Flow

### Chat Flow

```mermaid
sequenceDiagram
    participant User
    participant UI as Chat UI
    participant Store as Zustand
    participant Query as React Query
    participant API as API Client
    participant Backend

    User->>UI: Type question
    User->>UI: Click Send
    UI->>Store: Add user message
    UI->>Query: Trigger mutation
    Query->>API: POST /answer/{project_id}
    API->>Backend: Send request
    Backend-->>API: Return answer
    API-->>Query: Return data
    Query-->>UI: Update state
    UI->>Store: Add AI message
    UI-->>User: Display response
```

### File Upload Flow

```mermaid
sequenceDiagram
    participant User
    participant Dropzone as FileDropzone
    participant Query as React Query
    participant API as API Client
    participant Backend

    User->>Dropzone: Drop files
    Dropzone->>Query: Upload mutation
    Query->>API: POST /upload/{project_id}
    API->>Backend: Send file
    Backend-->>API: Return file_id
    API-->>Query: Return result
    Query-->>Dropzone: Show success
    Dropzone-->>User: Update file list
```

## Route Structure

| Route       | Component     | Description                |
| ----------- | ------------- | -------------------------- |
| `/`         | ChatPage      | Default chat interface     |
| `/upload`   | UploadPage    | File upload and processing |
| `/search`   | SearchPage    | Semantic search            |
| `/index`    | IndexInfoPage | Vector DB info             |
| `/settings` | SettingsPage  | App configuration          |

## State Management

### Server State (React Query)

```typescript
// Query Keys
['health'] - API health status
['index', projectId] - Index info
['search', projectId, query] - Search results

// Mutations
uploadFile - File upload
processFiles - Process chunks
pushToIndex - Vector DB indexing
getAnswer - RAG answer
```

### Client State (Zustand)

```typescript
interface SettingsStore {
  apiUrl: string;
  projectId: number;
  theme: "dark" | "light";
  chatHistory: ChatMessage[];
  setApiUrl: (url: string) => void;
  setProjectId: (id: number) => void;
  toggleTheme: () => void;
  addMessage: (msg: ChatMessage) => void;
  clearHistory: () => void;
}
```

## React Aria Components Usage

### Navigation

- `Tabs` - Main navigation between features
- `ListBox` - Project selector dropdown
- `Button` - Action buttons

### Chat

- `TextField` - Message input (multi-line)
- `Button` - Send button
- `ListBox` - Message list (virtualized)
- `Slider` - Context limit control

### Upload

- `DropZone` - File drop area
- `FileTrigger` - File picker button
- `ProgressBar` - Upload progress
- `Meter` - Processing progress
- `NumberField` - Chunk size input

### Search

- `SearchField` - Search input
- `Slider` - Results limit
- `GridList` - Results grid
- `Disclosure` - Expandable result details

### Settings

- `TextField` - API URL input
- `NumberField` - Project ID
- `Switch` - Theme toggle
- `Link` - External links
