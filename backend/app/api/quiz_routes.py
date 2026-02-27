"""
Quiz Routes - Handles adaptive quiz flows and answer submission
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.question import Question
from app.models.attempt import Attempt
from app.schemas.question_schema import QuestionForQuiz, SubmitAnswerRequest, DiagnosticCompleteRequest
from app.schemas.analytics_schema import RiskScoreResponse
from app.core.service_container import get_service_container
from app.core.exceptions import (
    NotFoundError,
    QuizSelectionError,
    PipelineError,
    ValidationError
)
from app.services.core.student_state import StudentState
from app.services.persistence.mastery_repository import MasteryRepository
from app.services.persistence.attempt_repository import AttemptRepository

router = APIRouter(prefix="/quiz", tags=["Quiz"])


def _get_or_create_student_state(db: Session, user_id: int) -> StudentState:
    """
    Get or create in-memory student state from database.
    This loads mastery, attempt history, and risk profile.
    """
    state = StudentState(student_id=user_id)
    
    # Load mastery from DB
    mastery_rows = db.query(Mastery).filter(Mastery.user_id == user_id).all()
    for row in mastery_rows:
        state.mastery_dict[row.concept] = row.mastery_value
        state.confidence_metrics[row.concept] = row.confidence
    
    # Load attempt history
    attempts = db.query(Attempt).filter(Attempt.user_id == user_id).all()
    for attempt in attempts:
        concept_row = db.query(Question).filter(Question.id == attempt.question_id).first()
        if concept_row:
            concept = concept_row.concept
            state.attempt_history.setdefault(concept, []).append(attempt.is_correct)
    
    # Load latest risk profile
    latest_risk = db.query(RiskHistory).filter(
        RiskHistory.student_id == str(user_id)
    ).order_by(RiskHistory.timestamp.desc()).first()
    
    if latest_risk:
        state.risk_profile = {
            "risk_probability": latest_risk.risk_score,
            "risk_label": latest_risk.risk_label,
            "risk_level": "high" if latest_risk.risk_score > 0.6 else "medium" if latest_risk.risk_score > 0.3 else "low"
        }
    
    return state


# Import at module level after function definitions
from app.models.mastery import Mastery
from app.models.risk_history import RiskHistory


@router.get("/questions/all")
def get_all_questions(
    limit: int = 500,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all questions grouped by concept (used for diagnostic test).
    Returns questions organized by concept with options.
    """
    try:
        questions = db.query(Question).limit(limit).all()
        
        if not questions:
            raise NotFoundError("Question", "any")
        
        # Group by concept
        questions_by_concept = {}
        for q in questions:
            if q.concept not in questions_by_concept:
                questions_by_concept[q.concept] = []
            
            options_list = q.options.split("||") if q.options else []
            correct_list = q.correct_answer.split("|") if q.correct_answer else []
            
            questions_by_concept[q.concept].append({
                "id": q.id,
                "topic": q.topic,
                "concept": q.concept,
                "difficulty": q.difficulty,
                "question_text": q.question_text,
                "question": q.question_text,  # Alias
                "options": options_list,
                "correct": correct_list,
                "multi": q.is_multiple == "true",
                "correct_answer": q.correct_answer
            })
        
        return questions_by_concept
    except NotFoundError:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get questions: {str(e)}")


@router.get("/questions/by-concept/{concept}")
def get_questions_by_concept(
    concept: str,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get questions for a specific concept.
    Returns questions with options.
    """
    try:
        questions = db.query(Question).filter(
            Question.concept == concept
        ).limit(limit).all()
        
        if not questions:
            raise NotFoundError("Question", f"with concept {concept}")
        
        result = []
        for q in questions:
            options_list = q.options.split("||") if q.options else []
            correct_list = q.correct_answer.split("|") if q.correct_answer else []
            
            result.append({
                "id": q.id,
                "topic": q.topic,
                "concept": q.concept,
                "difficulty": q.difficulty,
                "question_text": q.question_text,
                "question": q.question_text,  # Alias
                "options": options_list,
                "correct": correct_list,
                "multi": q.is_multiple == "true",
                "correct_answer": q.correct_answer
            })
        
        return result
    except NotFoundError:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get questions: {str(e)}")


@router.get("/has-attempted")
def check_has_attempted_quiz(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Check if user has attempted a quiz
    """
    attempt_count = db.query(Attempt).filter(Attempt.user_id == current_user.id).count()
    return {"has_attempted": attempt_count > 0}


@router.post("/diagnostic/complete")
def complete_diagnostic_quiz(
    request_data: DiagnosticCompleteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Mark diagnostic quiz as complete and save initial mastery assessment.
    This creates the initial student data table for the teacher to see.
    """
    try:
        mastery_scores = request_data.mastery_scores
        
        # Save mastery for each concept from diagnostic
        for concept, mastery_data in mastery_scores.items():
            mastery_value = mastery_data.get("value", 0.5) if isinstance(mastery_data, dict) else 0.5
            confidence = mastery_data.get("confidence", 0.5) if isinstance(mastery_data, dict) else 0.5
            
            # Check if mastery for this concept already exists
            existing = db.query(Mastery).filter(
                Mastery.user_id == current_user.id,
                Mastery.concept == concept
            ).first()
            
            if existing:
                # Update with diagnostic results
                existing.mastery_value = mastery_value
                existing.confidence = confidence
            else:
                # Create new mastery record
                new_mastery = Mastery(
                    user_id=current_user.id,
                    concept=concept,
                    mastery_value=mastery_value,
                    confidence=confidence
                )
                db.add(new_mastery)
        
        db.commit()
        return {"success": True, "message": "Diagnostic quiz results saved"}
    
    except Exception as e:
        db.rollback()
        print(f"Error saving diagnostic: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to save diagnostic results: {str(e)}")




def get_next_question(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get next question adapted to student's mastery level.
    Uses the adaptive logic engine to select based on:
    - Current mastery scores
    - Weakness in concepts
    - Recent performance
    """
    try:
        services = get_service_container(db)
        
        # Get student state
        student_state = _get_or_create_student_state(db, current_user.id)
        
        if not student_state.mastery_dict:
            # Cold start - select from all difficulty levels
            question = db.query(Question).filter(
                Question.difficulty.in_([1, 2, 3, 4, 5])
            ).first()
            if not question:
                raise NotFoundError("Question", "any")
        else:
            # Get adaptive logic recommendation
            weakest_concept = min(
                student_state.mastery_dict.items(),
                key=lambda x: x[1]
            )[0] if student_state.mastery_dict else None
            
            # Select question from weakest concept
            question = db.query(Question).filter(
                Question.concept == weakest_concept
            ).first()
            
            if not question:
                # Fallback to any random question
                question = db.query(Question).first()
        
        if not question:
            raise NotFoundError("Question", "any_available")
        
        return QuestionForQuiz(
            id=question.id,
            topic=question.topic,
            concept=question.concept,
            difficulty=question.difficulty,
            question_text=question.question_text
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get next question: {str(e)}")


@router.post("/submit")
def submit_answer(
    request: SubmitAnswerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submit an answer to a quiz question.
    
    This triggers the complete cognitive pipeline:
    1. Check if answer is correct
    2. Apply decay to all concepts
    3. Update mastery using BKT
    4. Recalculate confidence
    5. Propagate dependencies
    6. Extract risk features
    7. Predict risk
    8. Generate analytics insights
    
    Returns updated mastery, risk score, and next question metadata.
    """
    try:
        # Validate input
        if not request.response_time or request.response_time < 0:
            raise ValidationError("response_time must be positive")
        if not (1 <= request.confidence <= 10):
            raise ValidationError("confidence must be between 1-10")
        
        # Get question
        question = db.query(Question).filter(Question.id == request.question_id).first()
        if not question:
            raise NotFoundError("Question", request.question_id)
        
        # Check if answer is correct
        is_correct = request.user_answer.strip().lower() == question.correct_answer.strip().lower()
        
        # Get service container
        services = get_service_container(db)
        
        # Get or create student state
        student_state = _get_or_create_student_state(db, current_user.id)
        
        # Initialize concept if not seen before
        concept = question.concept
        if concept not in student_state.mastery_dict:
            student_state.mastery_dict[concept] = 0.5
            student_state.confidence_metrics[concept] = 0.5
        
        # Get total attempts for this concept
        total_attempts = len(student_state.attempt_history.get(concept, []))
        
        # Process through cognitive pipeline
        class_states = {}  # Placeholder for class-level state
        
        try:
            pipeline_result = services.pipeline.process_submission(
                user_id=current_user.id,
                student_state=student_state,
                concept=concept,
                correct=is_correct,
                response_time=request.response_time,
                student_confidence=request.confidence / 10.0,  # Convert 1-10 to 0-1
                total_attempts=total_attempts,
                class_states=class_states
            )
        except Exception as e:
            raise PipelineError(f"Pipeline processing failed: {str(e)}")
        
        # Store attempt in database
        attempt = Attempt(
            user_id=current_user.id,
            question_id=request.question_id,
            is_correct=is_correct,
            confidence=request.confidence
        )
        db.add(attempt)
        
        # Store updated mastery values
        for concept_name, mastery_value in student_state.mastery_dict.items():
            MasteryRepository.upsert_mastery(
                db,
                current_user.id,
                concept_name,
                mastery_value,
                student_state.confidence_metrics.get(concept_name, 0.5)
            )
        
        # Store risk score to database for real-time analytics
        if student_state.risk_profile:
            risk_entry = RiskHistory(
                student_id=str(current_user.id),
                risk_label=student_state.risk_profile.get("risk_label", 0),
                risk_score=float(student_state.risk_profile.get("risk_probability", 0))
            )
            db.add(risk_entry)
        
        db.commit()
        
        # Return response with updated state
        return {
            "is_correct": is_correct,
            "correct_answer": question.correct_answer,
            "mastery_update": {
                "concept": concept,
                "new_value": student_state.mastery_dict[concept],
                "delta": student_state.mastery_dict[concept] - (pipeline_result.get("old_mastery", 0.5) if pipeline_result else 0.5)
            },
            "risk_score": float(student_state.risk_profile.get("risk_probability", 0)) if student_state.risk_profile else 0,
            "risk_level": student_state.risk_profile.get("risk_level", "low") if student_state.risk_profile else "low",
            "confidence": student_state.confidence_metrics.get(concept, 0.5),
            "pipeline_result": pipeline_result
        }
    
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except PipelineError as e:
        raise HTTPException(status_code=500, detail=e.message)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit answer: {str(e)}")


@router.get("/risk-score")
def get_risk_score(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> RiskScoreResponse:
    """
    Get current risk score for the student.
    """
    try:
        student_state = _get_or_create_student_state(db, current_user.id)
        
        if not student_state.risk_profile:
            risk_profile = {
                "risk_probability": 0.0,
                "risk_level": "low",
                "confidence_score": 0.0,
                "feature_vector": [],
                "risk_label": "low"
            }
        else:
            risk_profile = student_state.risk_profile
        
        return RiskScoreResponse(
            user_id=current_user.id,
            risk_score=float(risk_profile.get("risk_probability", 0.0)),
            risk_label=risk_profile.get("risk_level", "low"),
            risk_factors={}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get risk score: {str(e)}")


@router.get("/explanation/{question_id}")
def get_explanation(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generate adaptive explanation for a question.
    Uses LLM-based explanation generator.
    """
    try:
        question = db.query(Question).filter(Question.id == question_id).first()
        if not question:
            raise NotFoundError("Question", question_id)
        
        services = get_service_container(db)
        student_state = _get_or_create_student_state(db, current_user.id)
        
        # Get mastery for this concept
        mastery_score = student_state.mastery_dict.get(question.concept, 0.5)
        weak_topics = [
            concept for concept, value in student_state.mastery_dict.items()
            if value < 0.4
        ]
        
        exp_gen = services.explanation_generator
        if not exp_gen:
            # Fallback explanation if LLM not available
            return {
                "explanation": f"To solve this {question.concept} problem, review the fundamentals and try similar practice problems.",
                "source": "fallback"
            }
        
        explanation = exp_gen.generate_adaptive_explanation(
            question={
                "question_text": question.question_text,
                "options": [],  # Adjust based on actual question format
                "base_explanation": ""
            },
            student_answer="",
            mastery_score=mastery_score,
            weak_topics=weak_topics,
            confidence_score=student_state.confidence_metrics.get(question.concept, 0.5)
        )
        
        return {
            "explanation": explanation,
            "concept": question.concept,
            "mastery_level": mastery_score
        }
    
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate explanation: {str(e)}")
