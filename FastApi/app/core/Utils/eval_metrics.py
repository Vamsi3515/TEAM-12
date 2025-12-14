"""Evaluation metrics for assessing AI agent performance.

This module provides various metrics to evaluate the quality of predictions
from ATS and GitHub analysis agents against expected outputs.
"""

from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def score_accuracy(
    predicted_score: float,
    expected_min: float,
    expected_max: float
) -> Dict[str, Any]:
    """Check if predicted score falls within expected range.
    
    Args:
        predicted_score: The score predicted by the agent
        expected_min: Minimum acceptable score
        expected_max: Maximum acceptable score
        
    Returns:
        Dictionary with 'passed', 'predicted', 'expected_range', and 'error'
    """
    passed = expected_min <= predicted_score <= expected_max
    
    # Calculate error (0 if within range, otherwise distance from nearest boundary)
    if passed:
        error = 0.0
    elif predicted_score < expected_min:
        error = expected_min - predicted_score
    else:
        error = predicted_score - expected_max
    
    return {
        "passed": passed,
        "predicted": predicted_score,
        "expected_range": {"min": expected_min, "max": expected_max},
        "error": error,
        "accuracy": 1.0 if passed else max(0.0, 1.0 - (error / 100.0))
    }


def keyword_overlap(
    predicted_list: List[str],
    expected_list: List[str],
    case_sensitive: bool = False
) -> Dict[str, Any]:
    """Calculate Jaccard similarity between predicted and expected keyword lists.
    
    Jaccard similarity = |intersection| / |union|
    
    Args:
        predicted_list: List of predicted keywords/items
        expected_list: List of expected keywords/items
        case_sensitive: Whether to consider case in comparisons
        
    Returns:
        Dictionary with 'jaccard_score', 'matched', 'missing', 'extra'
    """
    # Normalize for comparison
    if not case_sensitive:
        pred_set = {item.lower().strip() for item in predicted_list}
        exp_set = {item.lower().strip() for item in expected_list}
    else:
        pred_set = {item.strip() for item in predicted_list}
        exp_set = {item.strip() for item in expected_list}
    
    # Calculate Jaccard similarity
    intersection = pred_set & exp_set
    union = pred_set | exp_set
    
    jaccard_score = len(intersection) / len(union) if union else 0.0
    
    # Identify differences
    matched = list(intersection)
    missing = list(exp_set - pred_set)
    extra = list(pred_set - exp_set)
    
    return {
        "jaccard_score": jaccard_score,
        "matched": matched,
        "missing": missing,
        "extra": extra,
        "precision": len(intersection) / len(pred_set) if pred_set else 0.0,
        "recall": len(intersection) / len(exp_set) if exp_set else 0.0
    }


def substring_match(
    predicted_list: List[str],
    expected_list: List[str],
    case_sensitive: bool = False
) -> Dict[str, Any]:
    """Check if expected keywords appear as substrings in predicted items.
    
    Useful when expected items might be partial matches (e.g., "python" in "python experience").
    
    Args:
        predicted_list: List of predicted items
        expected_list: List of expected keywords to find
        case_sensitive: Whether to consider case
        
    Returns:
        Dictionary with match statistics
    """
    # Normalize
    predicted_str = " ".join(predicted_list)
    if not case_sensitive:
        predicted_str = predicted_str.lower()
        expected_list = [item.lower() for item in expected_list]
    
    matched = []
    missing = []
    
    for expected_item in expected_list:
        if expected_item in predicted_str:
            matched.append(expected_item)
        else:
            missing.append(expected_item)
    
    match_rate = len(matched) / len(expected_list) if expected_list else 0.0
    
    return {
        "match_rate": match_rate,
        "matched": matched,
        "missing": missing,
        "total_expected": len(expected_list)
    }


def semantic_similarity(
    predicted_text: str,
    expected_text: str,
    embedding_func: Optional[callable] = None
) -> Dict[str, Any]:
    """Calculate semantic similarity between predicted and expected text using embeddings.
    
    Args:
        predicted_text: Predicted text
        expected_text: Expected text
        embedding_func: Function to generate embeddings (defaults to simple word overlap)
        
    Returns:
        Dictionary with 'similarity_score' and 'method'
    """
    if embedding_func:
        # Use provided embedding function
        try:
            pred_emb = embedding_func([predicted_text])[0]
            exp_emb = embedding_func([expected_text])[0]
            
            # Reshape for cosine_similarity
            pred_emb = np.array(pred_emb).reshape(1, -1)
            exp_emb = np.array(exp_emb).reshape(1, -1)
            
            similarity = float(cosine_similarity(pred_emb, exp_emb)[0][0])
            
            return {
                "similarity_score": similarity,
                "method": "embedding_cosine"
            }
        except Exception as e:
            # Fall back to simple method
            pass
    
    # Simple word overlap as fallback
    pred_words = set(predicted_text.lower().split())
    exp_words = set(expected_text.lower().split())
    
    if not pred_words or not exp_words:
        return {"similarity_score": 0.0, "method": "word_overlap"}
    
    intersection = pred_words & exp_words
    union = pred_words | exp_words
    
    similarity = len(intersection) / len(union)
    
    return {
        "similarity_score": similarity,
        "method": "word_overlap"
    }


def json_structure_validity(
    output: Dict[str, Any],
    required_fields: List[str],
    optional_fields: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Validate JSON output structure against expected schema.
    
    Args:
        output: The JSON output to validate
        required_fields: List of required field names
        optional_fields: List of optional field names
        
    Returns:
        Dictionary with validation results
    """
    optional_fields = optional_fields or []
    
    missing_required = [field for field in required_fields if field not in output]
    present_required = [field for field in required_fields if field in output]
    present_optional = [field for field in optional_fields if field in output]
    
    # Check for unexpected fields
    expected_all = set(required_fields + optional_fields)
    unexpected = [field for field in output.keys() if field not in expected_all]
    
    valid = len(missing_required) == 0
    
    return {
        "valid": valid,
        "missing_required": missing_required,
        "present_required": present_required,
        "present_optional": present_optional,
        "unexpected_fields": unexpected,
        "completeness": len(present_required) / len(required_fields) if required_fields else 1.0
    }


def response_time_check(
    duration_ms: float,
    threshold_ms: float
) -> Dict[str, Any]:
    """Check if response time is within acceptable threshold.
    
    Args:
        duration_ms: Actual response time in milliseconds
        threshold_ms: Maximum acceptable time in milliseconds
        
    Returns:
        Dictionary with performance check results
    """
    passed = duration_ms <= threshold_ms
    
    # Calculate how much faster/slower than threshold
    ratio = duration_ms / threshold_ms if threshold_ms > 0 else float('inf')
    
    return {
        "passed": passed,
        "duration_ms": duration_ms,
        "threshold_ms": threshold_ms,
        "ratio": ratio,
        "status": "pass" if passed else "slow"
    }


def list_field_comparison(
    predicted: List[Any],
    expected: List[Any],
    partial_match: bool = True
) -> Dict[str, Any]:
    """Compare two list fields with flexible matching.
    
    Args:
        predicted: Predicted list
        expected: Expected list
        partial_match: Whether to allow partial substring matches
        
    Returns:
        Comparison metrics
    """
    if partial_match:
        # Use substring matching for more flexible comparison
        return substring_match(
            [str(item) for item in predicted],
            [str(item) for item in expected]
        )
    else:
        # Exact keyword matching
        return keyword_overlap(
            [str(item) for item in predicted],
            [str(item) for item in expected]
        )


def aggregate_metrics(metric_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Aggregate multiple metric results into summary statistics.
    
    Args:
        metric_results: List of individual metric result dictionaries
        
    Returns:
        Aggregated statistics
    """
    if not metric_results:
        return {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "pass_rate": 0.0
        }
    
    total = len(metric_results)
    passed = sum(1 for result in metric_results if result.get("passed", False))
    failed = total - passed
    
    # Calculate average scores for various metrics
    scores = []
    for result in metric_results:
        if "accuracy" in result:
            scores.append(result["accuracy"])
        elif "jaccard_score" in result:
            scores.append(result["jaccard_score"])
        elif "similarity_score" in result:
            scores.append(result["similarity_score"])
        elif "match_rate" in result:
            scores.append(result["match_rate"])
    
    avg_score = sum(scores) / len(scores) if scores else 0.0
    
    return {
        "total_tests": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": passed / total if total > 0 else 0.0,
        "average_score": avg_score
    }


def calculate_precision_recall_f1(
    true_positives: int,
    false_positives: int,
    false_negatives: int
) -> Dict[str, float]:
    """Calculate precision, recall, and F1 score.
    
    Args:
        true_positives: Number of correct positive predictions
        false_positives: Number of incorrect positive predictions
        false_negatives: Number of missed positive cases
        
    Returns:
        Dictionary with precision, recall, and F1 scores
    """
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return {
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    }
