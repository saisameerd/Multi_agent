import csv
import io
from typing import List, Dict, Any
from google.adk.artifacts import Artifact, ArtifactType

def csv_artifact_tool(csv_content: str, filename: str = "dialogflow_cx_training_phrases.csv") -> Artifact:
    """
    Creates a downloadable CSV artifact for Dialogflow CX training phrases.
    
    Args:
        csv_content: The CSV content as a string
        filename: The filename for the downloadable file
    
    Returns:
        Artifact: A downloadable CSV file artifact
    """
    # Create a CSV file in memory
    csv_buffer = io.StringIO(csv_content)
    
    # Create the artifact
    artifact = Artifact(
        type=ArtifactType.FILE,
        name=filename,
        description="Dialogflow CX training phrases CSV file for import",
        content=csv_buffer.getvalue().encode('utf-8'),
        mime_type="text/csv"
    )
    
    return artifact 