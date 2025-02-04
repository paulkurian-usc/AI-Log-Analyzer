# AI Log Analyzer

AI Log Analyzer is a powerful tool that uses GPT-4 to analyze log files, extract errors, and provide detailed analysis including root causes and solutions.

## Features

- Automatic error detection and extraction from log files
- Comprehensive error analysis using OpenAI's GPT-4
- Multiple error pattern recognition
- Detailed reporting with timestamps
- Debug mode for troubleshooting
- Environment variable configuration for secure API key management

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-log-analyzer.git
cd ai-log-analyzer
```

2. Install required dependencies:
```bash
pip install openai python-dotenv
```

3. Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

1. Place your log file in the project directory (default name: `error.log`)

2. Run the analyzer:
```bash
python log_analyzer.py
```

3. Find the analysis report in `log_analysis_report.txt`

## Error Analysis

The tool provides detailed analysis including:
- Error Type Classification
- Root Cause Identification
- Impact Assessment
- Solution Steps
- Prevention Recommendations

## Debug Mode

Enable debug mode to see detailed processing information:
```python
analyzer = LogAnalyzer()
analyzer.enable_debug()
```

## Configuration

The tool supports the following environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key (required)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for providing the GPT-4 API

## Security Note

Never commit your `.env` file or expose your API keys. The `.env` file is included in `.gitignore` by default.
