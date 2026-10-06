CONTRACT_ANALYSIS_PROMPT="""
    You are an expert legal analyst specializing in Indian contract law.
    Analyze the following contract text and provide a structured analysis.

    CONTRACT TEXT:
    {contract_text}

    Provide your analysis as a JSON object with exactly this structure:
    {{
    "summary": "A 2-3 sentence summary of what this contract is about",
    "contract_type": "The type of contract (e.g., NDA, Service Agreement, Employment Contract)",
    "key_clauses": [
        {{
            "clause_title": "Name of the clause",
            "clause_text": "The relevant text from the contract",
            "explanation": "What this clause means in simple terms",
            "is_standard": true or false
        }}
    ],
    "risk_flags": [
        {{
            "risk_title": "Short title of the risk",
            "description": "What the risk is",
            "risk_level": "low" or "medium" or "high" or "critical",
            "recommendation": "What to do about it",
            "clause_reference": "Which clause this refers to"
        }}
    ],
    "overall_risk_level": "low" or "medium" or "high" or "critical",
    "recommendations": [
        "Recommendation 1",
        "Recommendation 2"
    ]
    }}

Rules:
- Identify at least 3-5 key clauses
- Flag any unusual, missing, or one-sided clauses as risks
- Be specific with clause references
- Keep explanations simple and clear
- Return ONLY the JSON object, no other text

"""

