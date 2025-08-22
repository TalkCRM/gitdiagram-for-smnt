from fastapi import APIRouter, Request, HTTPException
from dotenv import load_dotenv

# from app.services.claude_service import ClaudeService
# from app.core.limiter import limiter
from anthropic._exceptions import RateLimitError
from app.prompts import SYSTEM_MODIFY_PROMPT
from app.utils.mermaid_validator import MermaidValidator, fix_common_mermaid_issues
from pydantic import BaseModel
from app.services.o1_mini_openai_service import OpenAIO1Service


load_dotenv()

router = APIRouter(prefix="/modify", tags=["Claude"])

# Initialize services
# claude_service = ClaudeService()
o1_service = OpenAIO1Service()


# Define the request body model


class ModifyRequest(BaseModel):
    instructions: str
    current_diagram: str
    repo: str
    username: str
    explanation: str


@router.post("")
# @limiter.limit("2/minute;10/day")
async def modify(request: Request, body: ModifyRequest):
    try:
        # Check instructions length
        if not body.instructions or not body.current_diagram:
            return {"error": "Instructions and/or current diagram are required"}
        elif (
            len(body.instructions) > 1000 or len(body.current_diagram) > 100000
        ):  # just being safe
            return {"error": "Instructions exceed maximum length of 1000 characters"}

        if body.repo in [
            "fastapi",
            "streamlit",
            "flask",
            "api-analytics",
            "monkeytype",
        ]:
            return {"error": "Example repos cannot be modified"}

        # modified_mermaid_code = claude_service.call_claude_api(
        #     system_prompt=SYSTEM_MODIFY_PROMPT,
        #     data={
        #         "instructions": body.instructions,
        #         "explanation": body.explanation,
        #         "diagram": body.current_diagram,
        #     },
        # )

        modified_mermaid_code = o1_service.call_o1_api(
            system_prompt=SYSTEM_MODIFY_PROMPT,
            data={
                "instructions": body.instructions,
                "explanation": body.explanation,
                "diagram": body.current_diagram,
            },
        )

        # Check for BAD_INSTRUCTIONS response
        if "BAD_INSTRUCTIONS" in modified_mermaid_code:
            return {"error": "Invalid or unclear instructions provided"}

        # Validate the modified mermaid code
        validator = MermaidValidator()
        is_valid, errors, warnings = validator.validate(modified_mermaid_code)
        
        if not is_valid:
            # Try to auto-fix
            fixed_code = fix_common_mermaid_issues(modified_mermaid_code)
            is_valid_fixed, _, _ = validator.validate(fixed_code)
            
            if is_valid_fixed:
                modified_mermaid_code = fixed_code
            else:
                # Regenerate with stricter prompt
                strict_prompt = SYSTEM_MODIFY_PROMPT + f"""

CRITICAL: Fix these syntax errors from the previous attempt:
{chr(10).join(errors)}
"""
                
                modified_mermaid_code = o1_service.call_o1_api(
                    system_prompt=strict_prompt,
                    data={
                        "instructions": body.instructions,
                        "explanation": body.explanation,
                        "diagram": body.current_diagram,
                    },
                )
                
                # Final auto-fix attempt
                modified_mermaid_code = fix_common_mermaid_issues(modified_mermaid_code)

        return {"diagram": modified_mermaid_code}
    except RateLimitError as e:
        raise HTTPException(
            status_code=429,
            detail="Service is currently experiencing high demand. Please try again in a few minutes.",
        )
    except Exception as e:
        return {"error": str(e)}
