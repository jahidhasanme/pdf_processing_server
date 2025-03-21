# Genrivia Backend

Genrivia Backend is a Python Flask application integrated with Agno for AI capabilities, AWS S3 for storage, and PostgreSQL for database management. This backend service supports the Genrivia frontend application.

## Features

- **Flask**: A lightweight WSGI web application framework in Python.
- **Agno**: AI integration for enhanced backend capabilities.
- **AWS S3**: Integration with Amazon S3 for scalable storage solutions.
- **PostgreSQL**: A powerful, open-source relational database system.

## Getting Started

### Prerequisites

- Python 3.8+
- pip
- AWS account
- PostgreSQL database

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/jahid-git/genrivia.git
    cd genrivia/server
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:

    Create a `.env` file in the root directory and add the following:

    ```env
    OPENAI_API_KEY=your-openai-api-key
    GEMINI_API_KEY=your-gemini-api-key
    FIREWORKS_API_KEY=your-aws-access-key-id
    GROQ_API_KEY=your-groq-api-key
    ```

### Running the Application

1. Start the Flask development server:

    ```bash
    python run.py
    ```

2. The backend server will be running at [http://localhost:5000](http://localhost:5000).

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.

## Contact

For any inquiries, please contact [jahidsite0@gmail.com](