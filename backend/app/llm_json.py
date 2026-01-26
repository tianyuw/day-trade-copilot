import json
from typing import Any
 
 
def _strip_code_fence(text: str) -> str:
    t = text.strip()
    if not t.startswith("```"):
        return t
 
    lines = t.splitlines()
    if not lines:
        return t
 
    if lines[0].lstrip().startswith("```"):
        lines = lines[1:]
 
    if lines and lines[-1].strip().startswith("```"):
        lines = lines[:-1]
 
    return "\n".join(lines).strip()
 
 
def parse_llm_json(text: str) -> Any:
    if text is None:
        raise ValueError("LLM returned empty response content")
 
    t = _strip_code_fence(text)
    if not t:
        raise ValueError("LLM returned empty response content")
 
    decoder = json.JSONDecoder()
 
    def _parse_from(s: str, start: int) -> tuple[Any, int]:
        obj, end_idx = decoder.raw_decode(s, idx=start)
        tail = s[end_idx:]
        if tail.strip() == "":
            return obj, end_idx
        if tail.strip() == "}":
            return obj, end_idx
        raise json.JSONDecodeError("Extra data", s, end_idx)
 
    try:
        obj, _ = _parse_from(t, 0)
        return obj
    except json.JSONDecodeError:
        first_obj = t.find("{")
        first_arr = t.find("[")
        starts = [i for i in [first_obj, first_arr] if i != -1]
        if not starts:
            raise
        start = min(starts)
        obj, _ = _parse_from(t, start)
        return obj
