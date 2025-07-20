#!/bin/bash

# Load .env.local if it exists
[ -f .env.local ] && source .env.local
openapi-typescript "$VITE_OPENAPI_URL" --output types/api.ts
