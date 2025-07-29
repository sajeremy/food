# Food Receipt Parser

A full-stack web application that uses AI to parse grocery receipt images and extract structured data for food tracking and analysis.

## Overview

This application allows users to upload grocery receipt images (including HEIC format) and automatically extract structured information about purchased items, prices, and store details using Google's Gemini AI model.

## Screenshots

### Receipt Upload Interface
![Upload Page](docs/images/upload-page.png)

The main upload interface features the "ShopSync" branding and allows users to drag and drop receipt images or click to browse files. It supports JPG, PNG, and HEIC formats up to 10MB, with navigation options for Dashboard, Trends, and Store Finder.

### Receipt Review Modal
![Receipt Review](docs/images/receipt-review.png)

After parsing, users can review the extracted data in a comprehensive side-by-side modal showing the original receipt image and the parsed item details including prices, quantities, categories (dairy, canned, meat, produce), and a "Save Receipt" option.

## Architecture

### Backend (`/backend`)

- **Framework**: FastAPI with Python 3.11+
- **AI Integration**: Google Gemini 2.0 Flash for receipt parsing
- **Database**: PostgreSQL with SQLModel ORM
- **Image Processing**: Supports multiple formats including HEIC conversion

### Frontend (`/frontend`)

- **Framework**: React 19 with TypeScript
- **Styling**: TailwindCSS with shadcn/ui components
- **Build Tool**: Vite
- **Image Handling**: HEIC to JPEG conversion support

## Features

- **Receipt Upload**: Support for various image formats including HEIC
- **AI-Powered Parsing**: Uses Google Gemini to extract structured data from receipts
- **Data Review**: Interactive modal to review and edit parsed receipt data
- **Database Storage**: Persistent storage with duplicate detection
- **Modern UI**: Clean, responsive interface with dropdown navigation
- **Type Safety**: Full TypeScript support with auto-generated API types

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL database
- Google Gemini API key

### Backend Setup

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```

2. Install dependencies:

   ```bash
   uv sync
   ```

3. Set up environment variables (create `.env` file):

   ```env
   GOOGLE_API_KEY=your_gemini_api_key
   DATABASE_URL=postgresql://user:password@localhost/dbname
   ```

4. Create database tables:

   ```bash
   python scripts/create_tables.py
   ```

5. Run the development server:
   ```bash
   uv run fastapi dev main.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   yarn install
   ```

3. Generate API types:

   ```bash
   yarn generate-types
   ```

4. Start the development server:
   ```bash
   yarn dev
   ```

## API Endpoints

- `GET /api/v0/status` - Health check
- `POST /api/v0/grocery_receipt` - Parse grocery receipt image

## Development

### Code Quality

- **Backend**: Uses Ruff for linting and formatting
- **Frontend**: ESLint with TypeScript support
- **Types**: Auto-generated from OpenAPI schema
