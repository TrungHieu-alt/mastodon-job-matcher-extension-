"""Candidate matching logic using ChromaDB and LLM."""

import json
from typing import List, Dict, Any
from loguru import logger

from db.cv_storage import search_similar_cvs
from utils.llm_utils import evaluate_candidate_with_llm


def find_matching_candidates(job_description: str, max_candidates: int = 5) -> List[Dict[str, Any]]:
    """Find matching candidates for a job description."""
    try:
        logger.info("Starting candidate matching process")
        
        # Step 1: Search for similar CVs using ChromaDB
        similar_cvs = search_similar_cvs(
            query=job_description,
            n_results=max_candidates * 2,
            similarity_threshold=0.6
        )
        
        if not similar_cvs:
            logger.warning("No similar CVs found")
            return []
        
        logger.info(f"Found {len(similar_cvs)} similar CVs from ChromaDB")
        
        # Step 2: Evaluate candidates with LLM
        evaluated_candidates = []
        for candidate in similar_cvs[:max_candidates]:
            try:
                evaluation = evaluate_candidate_with_llm(job_description, candidate)
                if evaluation:
                    candidate['llm_evaluation'] = evaluation
                    candidate['llm_score'] = evaluation.get('score', 0)
                    evaluated_candidates.append(candidate)
                else:
                    # Add candidate without LLM evaluation
                    candidate['llm_evaluation'] = {'score': 0, 'error': 'Evaluation failed'}
                    candidate['llm_score'] = 0
                    evaluated_candidates.append(candidate)
                    
            except Exception as e:
                logger.error(f"Error evaluating candidate: {e}")
                candidate['llm_evaluation'] = {'score': 0, 'error': str(e)}
                candidate['llm_score'] = 0
                evaluated_candidates.append(candidate)
        
        # Step 3: Sort by LLM score
        evaluated_candidates.sort(
            key=lambda x: x.get('llm_score', 0),
            reverse=True
        )
        
        logger.info(f"Completed matching: {len(evaluated_candidates)} candidates evaluated")
        return evaluated_candidates
        
    except Exception as e:
        logger.error(f"Error in candidate matching: {e}")
        return []


def calculate_composite_score(candidate: Dict[str, Any]) -> float:
    """Calculate composite score for a candidate."""
    try:
        similarity_score = candidate.get('similarity', 0)
        llm_score = candidate.get('llm_score', 0)
        
        # Weighted combination: 40% similarity + 60% LLM score
        composite_score = (similarity_score * 0.4) + (llm_score * 0.6)
        
        return composite_score
        
    except Exception as e:
        logger.error(f"Error calculating composite score: {e}")
        return 0.0
