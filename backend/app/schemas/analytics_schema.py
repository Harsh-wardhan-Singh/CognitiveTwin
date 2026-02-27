from pydantic import BaseModel
from typing import List, Dict, Optional


class InsightResponse(BaseModel):
    """Student insights from analytics engine"""
    weak_topics: List[str]
    calibration_gap: float
    learning_trend: Dict[str, float]
    volatility: Dict[str, float]
    recommended_topics: List[str]


class RiskScoreResponse(BaseModel):
    """Risk prediction for a student"""
    user_id: int
    risk_score: float  # 0-1 or 0-100
    risk_label: str  # "low", "medium", "high"
    risk_factors: Dict[str, float]


class ClassAnalyticsResponse(BaseModel):
    """Class-level analytics"""
    class_id: int
    average_mastery: float
    at_risk_count: int
    total_students: int
    weak_concepts: List[str]
    heatmap: Dict[str, float]


class DashboardResponse(BaseModel):
    """Complete student dashboard view"""
    user_id: int
    mastery: Dict[str, float]  # concept -> value
    risk_score: float
    insights: InsightResponse
    recent_attempts: List[Dict]
