# Response Comparator

A Python script that compares two responses to a given input message using the Perplexity AI API to determine which response is better.

## Features

- **File-based input**: Reads input and output messages from text files
- **Perplexity AI integration**: Uses Perplexity API for intelligent comparison
- **Environment variable support**: Loads API keys from `.env` file
- **Verbose output**: Optional detailed logging of the comparison process
- **JSON output**: Optional JSON formatted results
- **Error handling**: Robust error handling for file operations and API calls

## Installation

1. Clone the repository:
```bash
git clone https://github.com/subrat-kp/response-comparator.git
cd response-comparator
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root and add your Perplexity API key:
```env
PERPLEXITY_API_KEY=your-api-key-here
```

You can get your API key from [Perplexity AI](https://docs.perplexity.ai/).

## Usage

### Basic Usage
```bash
python message_comparator.py -i input.txt -a output_a.txt -b output_b.txt
```

### With Verbose Output
```bash
python message_comparator.py -i input.txt -a output_a.txt -b output_b.txt --verbose
```

### JSON Output
```bash
python message_comparator.py -i input.txt -a output_a.txt -b output_b.txt --json
```

### Command Line Options

- `-i, --input-file`: Path to the text file containing the input message
- `-a, --output-a-file`: Path to the text file containing the first output message
- `-b, --output-b-file`: Path to the text file containing the second output message
- `--verbose`: Enable verbose output with detailed logging
- `--json`: Output results in JSON format

## Example Files

The repository includes sample files to test the functionality:

**sample_input.txt:**
```
What is the best programming language for beginners to learn?
```

**sample_output_a.txt:**
```
Python is the best programming language for beginners because it has simple syntax, extensive libraries, and a large community. It's used in web development, data science, and automation.
```

**sample_output_b.txt:**
```
JavaScript is better for beginners since it runs in browsers and you can see immediate visual results. It's essential for web development and has many job opportunities.
```

### Running with Sample Files
```bash
python message_comparator.py -i sample_input.txt -a sample_output_a.txt -b sample_output_b.txt --verbose
```

## Output

The script will output one of the following results:
- **"A"**: If Output A is better
- **"B"**: If Output B is better  
- **"Both"**: If both outputs are equally good
- **"Neither"**: If both outputs are inadequate

Each result includes a brief explanation (1-2 sentences) for the choice.

## File Structure

```
response-comparator/
├── message_comparator.py     # Main script
├── requirements.txt          # Python dependencies
├── .env                     # Environment variables (not tracked)
├── .gitignore              # Git ignore rules
├── README.md               # This file
├── sample_input.txt        # Example input file
├── sample_output_a.txt     # Example output A file
└── sample_output_b.txt     # Example output B file
```

## Requirements

- Python 3.7+
- requests >= 2.32.0
- python-dotenv >= 1.0.0
- Valid Perplexity API key

## Error Handling

The script includes comprehensive error handling for:
- Missing or empty files
- Invalid file paths
- Missing API key
- Network connectivity issues
- SSL certificate problems (with automatic fallback)
- API rate limiting and errors

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.