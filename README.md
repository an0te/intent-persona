
# Search Intent & Motivation Analysis Tool

This is a Streamlit-based web application that leverages OpenAI's GPT-4 model to analyze search intent and generate detailed marketing personas based on a specified keyword. It provides insights into user intent and helps create targeted marketing strategies by generating personas and addressing key consumer questions and concerns.

## Features

- **Search Intent Analysis**: Analyzes the intent behind a given keyword.
- **Persona Generation**: Creates detailed personas based on the search intent.
- **Motivation Analysis**: Provides answers to key marketing questions based on the generated personas.
- **CSV Download**: Allows users to download the analysis results as a CSV file.

## Installation

To run this application locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/an0te/intent-persona
   cd search-intent-analysis
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Open the application in your web browser.
2. Enter your OpenAI API key in the sidebar.
3. Input the keyword you want to analyze.
4. Select the number of personas to generate.
5. View the generated search intent, personas, and detailed motivation analysis.
6. Download the analysis results as a CSV file.

## Dependencies

- `streamlit`: Web framework for creating interactive applications.
- `openai`: Python client for OpenAI's API.
- `pandas`: Data manipulation and analysis library.
- `streamlit-lottie`: Integration for Lottie animations in Streamlit.
- `requests`: HTTP library for Python.
- `streamlit-javascript`: JavaScript integration for Streamlit (if needed).


## Contributing

If you'd like to contribute to this project, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you'd like to change.

## License

This tool is based on a script originally published by Kristin Tynski

