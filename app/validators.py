import re
from typing import Dict, List, Tuple


class ValidationModule:
    """
    Validates input responses for quality and meaningfulness
    Ensures data is suitable for EQ analysis
    """
    
    @staticmethod
    def validate_response(response: str) -> Tuple[bool, str]:
        """
        Validate a single response
        Returns: (is_valid, message)
        """
        if not response:
            return False, "Response cannot be empty"
        
        if len(response) < 10:
            return False, "Response is too short. Please provide at least 10 characters."
        
        if len(response) > 1000:
            return False, "Response is too long. Please keep it under 1000 characters."
        
        # Check for meaningful content (not just random characters)
        if not ValidationModule._has_meaningful_content(response):
            return False, "Response appears to lack meaningful content."
        
        return True, "Valid response"
    
    @staticmethod
    def _has_meaningful_content(text: str) -> bool:
        """Check if text contains meaningful words"""
        # Remove special characters and convert to lowercase
        cleaned = re.sub(r'[^a-zA-Z\s]', '', text).lower()
        words = cleaned.split()
        
        # Must have at least 3 meaningful words
        return len(words) >= 3 and len(cleaned) > 5
    
    @staticmethod
    def validate_all_responses(responses: List[str]) -> Tuple[bool, List[str]]:
        """
        Validate all responses
        Returns: (all_valid, list_of_errors)
        """
        errors = []
        for i, response in enumerate(responses, 1):
            is_valid, message = ValidationModule.validate_response(response)
            if not is_valid:
                errors.append(f"Response {i}: {message}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Remove potentially harmful characters while preserving text"""
        # Remove HTML/SQL injection attempts
        text = re.sub(r'[<>\"\'%;()&+]', '', text)
        # Normalize whitespace
        text = ' '.join(text.split())
        return text.strip()
    
    @staticmethod
    def validate_user_info(name: str, age: str, gender: str, profession: str) -> Tuple[bool, List[str]]:
        """Validate user registration information"""
        errors = []
        
        # Validate name
        if not name or len(name) < 2:
            errors.append("Name must be at least 2 characters")
        
        # Validate age
        try:
            age_int = int(age)
            if age_int < 18 or age_int > 100:
                errors.append("Age must be between 18 and 100")
        except ValueError:
            errors.append("Age must be a valid number")
        
        # Validate gender
        if gender not in ['Male', 'Female', 'Other']:
            errors.append("Please select a valid gender option")
        
        # Validate profession
        valid_professions = ['Software Engineer', 'Doctor', 'Teacher', 'Manager', 'Sales Executive', 'Designer']
        if profession not in valid_professions:
            errors.append("Please select a valid profession")
        
        return len(errors) == 0, errors
