import os
from openai import OpenAI
from dotenv import load_dotenv
import re
from datetime import datetime

class LogAnalyzer:
    def __init__(self, api_key):
        load_dotenv()  # Load environment variables
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)
        self.debug_mode = False
        
    def enable_debug(self):
        self.debug_mode = True
        
    def debug_print(self, message):
        if self.debug_mode:
            print(f"[DEBUG] {message}")

    def extract_complete_error(self, log_content):
        """Extract the most recent complete error with full context."""
        self.debug_print("Extracting complete error context...")
        
        # Pattern to match different types of errors with their context
        error_patterns = [
            # Pattern for logs with [ERROR] tag and traceback
            r"(\[\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}.*?\] \[ERROR\].*?(?:Traceback.*?)(?:Error|Exception):.*?)(?=\[\d{4}-\d{2}-\d{2}|\Z)",
            
            # Pattern for standard Python tracebacks
            r"(Traceback \(most recent call last\):.*?(?:Error|Exception):.*?)(?=\[\d{4}-\d{2}-\d{2}|\Z)",
            
            # Pattern for any line containing ERROR or CRITICAL
            r"(\[\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}.*?\] \[(?:ERROR|CRITICAL)\].*?)(?=\[\d{4}-\d{2}-\d{2}|\Z)"
        ]
        
        all_errors = []
        for pattern in error_patterns:
            matches = list(re.finditer(pattern, log_content, re.DOTALL | re.MULTILINE))
            all_errors.extend(matches)
        
        if all_errors:
            # Sort errors by their position in the log file (to get the most recent)
            all_errors.sort(key=lambda x: x.start())
            last_error = all_errors[-1].group(1).strip()
            self.debug_print("Found error with complete context")
            return last_error
        
        self.debug_print("No errors found")
        return None

    def analyze_error(self, error_content):
        """Analyze any type of error with detailed context."""
        prompt = f"""Analyze this error from a log file. Please provide:
        1. Error Type: The specific type of error (e.g., SQL, Runtime, Network, etc.)
        2. Root Cause: What specifically caused this error
        3. Impact: What operation or functionality was affected
        4. Solution: Specific steps to fix this issue
        5. Prevention: How to prevent this in future

        Log content:
        {error_content}
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are an expert system analyst specializing in error diagnosis and debugging. Provide technical, actionable analysis focusing on the error and its context."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            self.debug_print(f"Error during API call: {str(e)}")
            return f"Error during analysis: {str(e)}"

    def generate_report(self, file_path):
        """Generate analysis report focusing on the most recent error."""
        start_time = datetime.now()
        self.debug_print("Starting report generation...")
        
        with open(file_path, 'r') as file:
            log_content = file.read()
            
        error_content = self.extract_complete_error(log_content)
        
        if not error_content:
            return "No errors found in the log file."
        
        report = f"""Log Analysis Report
        Generated: {start_time.strftime('%Y-%m-%d %H:%M:%S')}
        File Analyzed: {file_path}

        {'='*50}

        Most Recent Error:
        {error_content}

        {'='*50}

        Analysis:
        {self.analyze_error(error_content)}
        """
        
        self.debug_print("Report generation completed")
        return report

def main():
    # Replace with your OpenAI API key
    api_key = ""

    
    # Initialize analyzer
    analyzer = LogAnalyzer(api_key)
    analyzer.enable_debug()
    
    # Generate and save report
    report = analyzer.generate_report("error.log")
    with open("log_analysis_report.txt", 'w') as f:
        f.write(report)

if __name__ == "__main__":
    main()