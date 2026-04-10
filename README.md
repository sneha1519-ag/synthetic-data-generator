# Synthetic Data Generator 🧪

![Synthetic Data Generator](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/Frontend-React_19-61DAFB?logo=react&logoColor=black)
![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind_CSS-38B2AC?logo=tailwind-css&logoColor=white)
![AI](https://img.shields.io/badge/AI-Gemini_1.5_Pro-8E75B2?logo=google&logoColor=white)

A full-stack web application designed to generate highly realistic, customizable synthetic datasets for testing, machine learning, and development purposes. It provides programmatic data mocking via the `Faker` library, as well as AI-powered autonomous dataset creation using Google's Gemini LLM.

## 🚀 Features

- **Manual Data Generation**: Hand-pick from over 20 predefined data fields (names, emails, geospatial locations, IoT sensor readings, credit cards, etc.).
- **Quick Templates**: Apply instant templates for common use cases like *E-commerce*, *Healthcare*, *HR*, and *IoT logging*.
- **AI-Powered Generation**: Describe the data you want in plain text (e.g., _"Generate a dataset for an online clothing store..."_), and let Gemini 1.5 Pro autonomously structure and populate a tailored dataset!
- **Data Realism Modes**:
  - **Realistic**: Standard fake, yet highly plausible data.
  - **Randomized**: Completely randomized structural data.
  - **Biased**: Skewed data generation useful for simulating edge cases and stress testing (e.g., concentrated demographics or localized anomalies).
- **Data Download**: Preview generated data in the browser and export up to 10,000 rows as a standard CSV file directly to your machine.

## 🏗️ Architecture & Tech Stack

The application is segregated into a decoupled client-server architecture:

### Frontend
- **React.js (v19)**: Component-based UI scaling.
- **Tailwind CSS (v4)**: Rapid, utility-first UI styling.
- **Lucide React**: Crisp iconography styling.
- **Fetch API**: For async communication with the backend.

### Backend
- **FastAPI (Python)**: High-performance ASGI framework handling core API traffic.
- **Faker**: Powers the extensive programmatic simulation of manual fields.
- **Google GenAI SDK**: Interfaces with `gemini-1.5-pro` for intelligent prompting and structural JSON data rendering.
- **Pandas**: Efficient transformation of generated objects into scalable CSV streams.

## ⚙️ Getting Started

### Prerequisites
- Node.js (v16 or higher)
- Python (v3.9 or higher)
- Google Gemini API Key

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create python virtual environment (Optional but Recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies (Require FastAPI, uvicorn, faker, google-generativeai, pandas, pydantic):
   ```bash
   pip install -r requirements.txt
   ```
4. Configure application environment variables:
   Create a `.env` file in the `/backend` directory and add your Google API key:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```
5. Run the FastAPI development server:
   ```bash
   python -m uvicorn app:app --reload
   ```
   *(Or run `python app.py`)*
   *The backend will be live on `http://localhost:8000`*

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install Node dependencies:
   ```bash
   npm install
   ```
3. Boot up the React app in development mode:
   ```bash
   npm start
   ```
   *The frontend will dynamically run on `http://localhost:3000`*

## 📁 Project Structure

```text
synthetic-data-generator/
├── backend/
│   ├── app.py                 # FastAPI application entrypoint
│   ├── generators/            # Core logic for data simulation
│   │   ├── ai_generator.py    # Interfaces with Gemini API
│   │   ├── faker_generator.py # Interfaces with Python Faker
│   │   └── random_generator.py# Basic randomness handling
│   ├── models/                # Pydantic validation schemas
│   ├── utils/                 # Utilities for CSV transformations
│   └── temp_data/             # Temporary OS storage for generated CSVs
└── frontend/
    ├── public/                # Static files
    ├── src/
    │   ├── App.js             # Main frontend component logic
    │   ├── index.css          # Tailwind CSS configurations
    │   └── ...                # Standard React bootstrapping files
    ├── package.json           # Node configuration & scripts
    └── tailwind.config.js     # PostCSS/Tailwind integrations
```

## 🔐 API Documentation (Endpoints)
- `POST /api/generate-data` : Triggers the data generation task (accepts AI prompt or specific field lists). Returns dataset ID and sample data.
- `GET /api/download/{dataset_id}`: Initiates a direct CSV file download for the cached dataset.
- `DELETE /api/datasets/{dataset_id}`: Standard deletion route.

## 🤝 Contributing
Contributions, issues, and feature requests are always welcome! Feel free to check the issues page and open a pull request.

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.
