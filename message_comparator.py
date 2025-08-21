#!/usr/bin/env python3
"""
Message Comparator Script

This script takes an input message and two output messages from text files, then uses the Perplexity API
to determine which output is better (A or B) or returns an appropriate answer if neither is better.

Installation:
    pip install -r requirements.txt

Usage:
    python message_comparator.py --input-file input.txt --output-a-file output_a.txt --output-b-file output_b.txt
    python message_comparator.py -i input.txt -a output_a.txt -b output_b.txt

Environment Variables:
    PERPLEXITY_API_KEY: Your Perplexity API key (required)
    
You can set this in a .env file in the same directory as the script:
    PERPLEXITY_API_KEY=your-api-key-here
"""

import argparse
import os
import sys
import json
import requests
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class PerplexityClient:
    """Client for interacting with the Perplexity API."""
    
    def __init__(self, api_key: str):
        """Initialize the Perplexity client with API key."""
        self.api_key = api_key
        self.base_url = "https://api.perplexity.ai"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def compare_messages(self, input_message: str, output_a: str, output_b: str) -> Dict[str, Any]:
        """
        Compare two output messages using the Perplexity API.
        
        Args:
            input_message: The original input message
            output_a: First output message to compare
            output_b: Second output message to compare
            
        Returns:
            Dictionary containing the comparison result
        """
        prompt = f"""
Please analyze the following input message and two output responses, then determine which output is better.

Input Message: "{input_message}"

Output A: "{output_a}"

Output B: "{output_b}"

Please evaluate both outputs based on:
1. Relevance to the input message
2. Accuracy and correctness
3. Clarity and comprehensiveness
4. Helpfulness and usefulness

Respond with ONLY one of the following:
- "A" if Output A is better
- "B" if Output B is better  
- "Both" if both are equally good
- "Neither" if both outputs are bad or if neither adequately addresses the input

Provide a brief explanation (1-2 sentences) for your choice.
"""

        payload = {
            "model": "llama-3.1-sonar-small-128k-online",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert evaluator tasked with comparing two responses to determine which is better. Be objective and analytical in your assessment."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 200,
            "temperature": 0.1
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30,
                verify=True  # Enable SSL verification but handle errors gracefully
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.SSLError as e:
            # Retry with SSL verification disabled if certificate verification fails
            try:
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload,
                    timeout=30,
                    verify=False
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as retry_e:
                raise Exception(f"API request failed even with SSL verification disabled: {str(retry_e)}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")


class MessageComparator:
    """Main class for comparing messages using Perplexity API."""
    
    def __init__(self, api_key: str):
        """Initialize the message comparator."""
        self.client = PerplexityClient(api_key)
    
    def compare(self, input_message: str, output_a: str, output_b: str) -> str:
        """
        Compare two output messages and return the result.
        
        Args:
            input_message: The original input message
            output_a: First output message to compare
            output_b: Second output message to compare
            
        Returns:
            String indicating the comparison result and explanation
        """
        try:
            response = self.client.compare_messages(input_message, output_a, output_b)
            
            # Extract the content from the API response
            if 'choices' in response and len(response['choices']) > 0:
                content = response['choices'][0]['message']['content'].strip()
                return content
            else:
                return "Error: Unable to get a valid response from the API"
                
        except Exception as e:
            return f"Error during comparison: {str(e)}"


def validate_api_key() -> str:
    """Validate and return the API key from environment variables."""
    api_key = os.getenv('PERPLEXITY_API_KEY')
    if not api_key:
        print("Error: PERPLEXITY_API_KEY environment variable is required.")
        print("Please set it with: export PERPLEXITY_API_KEY='your-api-key-here'")
        sys.exit(1)
    return api_key


def read_file_content(file_path: str) -> str:
    """
    Read content from a text file.
    
    Args:
        file_path: Path to the text file
        
    Returns:
        Content of the file as a string
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        Exception: If there's an error reading the file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            if not content:
                raise Exception(f"File {file_path} is empty")
            return content
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error reading file {file_path}: {str(e)}")


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Compare two output messages using Perplexity API by reading from text files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python message_comparator.py -i input.txt -a output_a.txt -b output_b.txt
  python message_comparator.py --input-file input.txt --output-a-file output_a.txt --output-b-file output_b.txt
        """
    )
    
    parser.add_argument(
        '-i', '--input-file',
        required=True,
        help='Path to the text file containing the input message'
    )
    
    parser.add_argument(
        '-a', '--output-a-file',
        required=True,
        help='Path to the text file containing the first output message to compare'
    )
    
    parser.add_argument(
        '-b', '--output-b-file',
        required=True,
        help='Path to the text file containing the second output message to compare'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output result in JSON format'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    return parser.parse_args()


def main():
    """Main function."""
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Validate API key
        api_key = validate_api_key()
        
        if args.verbose:
            print("Initializing Message Comparator...")
            print(f"Reading input from: {args.input_file}")
            print(f"Reading output A from: {args.output_a_file}")
            print(f"Reading output B from: {args.output_b_file}")
            print()
        
        # Read content from files
        if args.verbose:
            print("Reading file contents...")
        
        input_message = read_file_content(args.input_file)
        output_a = read_file_content(args.output_a_file)
        output_b = read_file_content(args.output_b_file)
        
        if args.verbose:
            print(f"Input message: {input_message}")
            print(f"Output A: {output_a}")
            print(f"Output B: {output_b}")
            print()
        
        # Initialize comparator
        comparator = MessageComparator(api_key)
        
        # Perform comparison
        if args.verbose:
            print("Comparing messages using Perplexity API...")
        
        result = comparator.compare(input_message, output_a, output_b)
        
        # Output result
        if args.json:
            output = {
                "input_file": args.input_file,
                "output_a_file": args.output_a_file,
                "output_b_file": args.output_b_file,
                "input_message": input_message,
                "output_a": output_a,
                "output_b": output_b,
                "comparison_result": result
            }
            print(json.dumps(output, indent=2))
        else:
            print("Comparison Result:")
            print("-" * 50)
            print(result)
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()