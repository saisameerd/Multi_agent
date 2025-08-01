import csv
import io
import os
from typing import List, Dict, Any
from datetime import datetime

def csv_artifact_tool(csv_content: str, filename: str = "dialogflow_cx_training_phrases.csv") -> Dict[str, Any]:
    """
    Creates a CSV file for Dialogflow CX training phrases.
    
    This function creates a CSV file in the current directory and returns metadata about it.
    
    Args:
        csv_content: The CSV content as a string
        filename: The filename for the downloadable file
    
    Returns:
        Dict: Metadata about the created CSV file
    """
    try:
        # Create a CSV file in the current directory
        file_path = os.path.join(os.getcwd(), filename)
        
        # Write the CSV content to file
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            csvfile.write(csv_content)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Return metadata about the created file
        return {
            "status": "success",
            "message": f"CSV file created successfully: {filename}",
            "file_path": file_path,
            "file_size": file_size,
            "filename": filename,
            "created_at": datetime.now().isoformat(),
            "download_instructions": f"File saved to: {file_path}"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to create CSV file: {str(e)}",
            "error": str(e)
        }

def create_csv_content_from_data(data: List[Dict[str, Any]]) -> str:
    """
    Helper function to create CSV content from structured data.
    
    Args:
        data: List of dictionaries containing the data to convert to CSV
    
    Returns:
        str: CSV content as a string
    """
    if not data:
        return ""
    
    # Get fieldnames from the first item
    fieldnames = list(data[0].keys())
    
    # Create CSV content
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    
    # Write header
    writer.writeheader()
    
    # Write data rows
    writer.writerows(data)
    
    return output.getvalue()

# Example usage function
def generate_sample_csv() -> str:
    """
    Generate a sample CSV content for testing.
    
    Returns:
        str: Sample CSV content
    """
    sample_data = [
        {
            "Intent Name": "AccountSuspensionIntent",
            "Training Phrase": "Why is my account suspended?",
            "Priority": "High",
            "Category": "New Intent",
            "Description": "Handles account suspension queries"
        },
        {
            "Intent Name": "AccountSuspensionIntent",
            "Training Phrase": "My account got suspended",
            "Priority": "High",
            "Category": "New Intent",
            "Description": "Handles account suspension queries"
        },
        {
            "Intent Name": "PaymentIssueIntent",
            "Training Phrase": "I can't make a payment",
            "Priority": "Medium",
            "Category": "New Intent",
            "Description": "Handles payment-related issues"
        }
    ]
    
    return create_csv_content_from_data(sample_data) 