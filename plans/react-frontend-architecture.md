# Fehres React Frontend Architecture

## Overview

A modern, accessible Single Page Application (SPA) built with React, TypeScript, and React Aria components to replace the existing Streamlit frontend.

## Tech Stack

### Core Technologies

- **React 18+** - UI library with hooks
- **TypeScript** - Type safety
- **Vite** - Fast build tool and dev server
- **React Router v6** - Client-side routing

### UI & Accessibility

- **React Aria Components** - Accessible, unstyled UI primitives from Adobe
- **Tailwind CSS** - Utility-first styling
- **React Stately** - State management hooks from React Aria
- **Heroicons** - Consistent iconography

### Data & State

- **TanStack Query (React Query)** - Server state management
- **Axios** - HTTP client
- **Zustand** - Client state management (settings, theme)

### Developer Experience

- **ESLint** - Code linting
- **Prettier** - Code formatting
- **TypeScript** - Static type checking

## Project Structure

```
frontend/
├── public/
│   └── favicon.ico
├── src/
│   ├── api/
│   │   ├── client.ts          # Axios instance
│   │   ├── types.ts           # API response/request types
│   │   ├── data.ts            # Data API endpoints
│   │   ├── nlp.ts             # NLP API endpoints
│   │   └── base.ts            # Base/health endpoints
│   ├── components/
│   │   ├── ui/                # Reusable UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── FileDropzone.tsx
│   │   │   ├── StatusBadge.tsx
│   │   │   └── MetricCard.tsx
│   │   ├── layout/            # Layout components
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Header.tsx
│   │   │   └── MainLayout.tsx
│   │   └── features/          # Feature-specific components
│   │       ├── chat/
│   │       ├── upload/
│   │       ├── search/
│   │       └── index/
│   ├── hooks/
│   │   ├── useApi.ts          # API hooks
│   │   └── useSettings.ts     # Settings management
│   ├── pages/
│   │   ├── ChatPage.tsx
│   │   ├── UploadPage.tsx
│   │   ├── SearchPage.tsx
│   │   ├── IndexInfoPage.tsx
│   │   └── SettingsPage.tsx
│   ├── stores/
│   │   └── settingsStore.ts   # Zustand store
│   ├── types/
│   │   └── index.ts           # Shared TypeScript types
│   ├── utils/
│   │   └── helpers.ts         # Utility functions
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── index.html
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── vite.config.ts
```

## API Integration

### Endpoints Mapping

| Feature       | Endpoint                                | Method |
| ------------- | --------------------------------------- | ------ |
| Health Check  | `/api/v1/`                              | GET    |
| File Upload   | `/api/v1/data/upload/{project_id}`      | POST   |
| Process Files | `/api/v1/data/process/{project_id}`     | POST   |
| Push to Index | `/api/v1/nlp/index/push/{project_id}`   | POST   |
| Index Info    | `/api/v1/nlp/index/info/{project_id}`   | GET    |
| Search        | `/api/v1/nlp/index/search/{project_id}` | POST   |
| Answer (RAG)  | `/api/v1/nlp/index/answer/{project_id}` | POST   |

## Page Designs

### 1. Chat Page (Primary)

- **Purpose**: RAG Q&A interface
- **Layout**: Full-height chat interface
- **Components**:
  - Chat message list (virtualized for performance)
  - Message bubbles (user/AI distinction)
  - Input area with submit button
  - Context limit slider (React Aria Slider)
  - Clear history button
  - Loading indicators

### 2. Upload & Process Page

- **Purpose**: Document ingestion pipeline
- **Layout**: Multi-step wizard or tabbed interface
- **Components**:
  - File dropzone (React Aria DropZone)
  - File list with status
  - Processing controls (chunk size, overlap)
  - Progress indicators
  - Index push button

### 3. Search Page

- **Purpose**: Semantic document search
- **Layout**: Search bar + results grid
- **Components**:
  - Search input with suggestions
  - Results limit slider
  - Result cards with relevance score
  - Expandable result details

### 4. Index Info Page

- **Purpose**: Vector database statistics
- **Layout**: Dashboard with metrics
- **Components**:
  - Metric cards (total vectors, status, etc.)
  - Refresh button
  - JSON viewer for detailed info

### 5. Settings Page

- **Purpose**: App configuration
- **Layout**: Form with sections
- **Components**:
  - API URL input
  - Project ID selector
  - Theme toggle
  - Quick links section

## Design System

### Color Palette (Dark Mode First)

```
Primary:      #667eea (Indigo)
Secondary:    #764ba2 (Purple)
Success:      #2ed573 (Green)
Warning:      #ffa502 (Orange)
Error:        #ff4757 (Red)
Background:   #0f0f1a (Dark)
Surface:      #1a1a2e (Card)
Border:       rgba(255,255,255,0.1)
Text Primary: #ffffff
Text Muted:   rgba(255,255,255,0.7)
```

### Typography

- Font: Inter (Google Fonts)
- Headings: 600-700 weight
- Body: 400 weight
- Scale: 1.25 ratio

### Spacing

- Base unit: 4px
- Small: 8px
- Medium: 16px
- Large: 24px
- XLarge: 32px

## Accessibility Features

- Full keyboard navigation support
- ARIA labels and roles
- Focus management
- Screen reader announcements
- High contrast mode support
- Reduced motion preferences

## Responsive Breakpoints

- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

## State Management Strategy

### Server State (React Query)

- API responses
- Loading states
- Error handling
- Caching and invalidation

### Client State (Zustand)

- Settings (API URL, project ID)
- Theme preference
- UI state (sidebar open/closed)
- Chat history (local)

## Implementation Phases

### Phase 1: Foundation

1. Project setup with Vite + TypeScript
2. Install dependencies
3. Configure Tailwind + React Aria
4. Set up routing

### Phase 2: Core UI

1. Layout components (Sidebar, Header)
2. Design system components
3. API client setup

### Phase 3: Features

1. Chat page
2. Upload page
3. Search page
4. Index info page

### Phase 4: Polish

1. Error handling
2. Loading states
3. Animations
4. Responsive design

### Phase 5: Build & Deploy

1. Production build
2. Docker integration
3. Documentation
