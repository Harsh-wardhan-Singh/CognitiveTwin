from datetime import datetime


class QuizSession:
    """
    Tracks a student's live quiz session.
    """

    def __init__(self, student_id: str, quiz_id: str):
        self.student_id = student_id
        self.quiz_id = quiz_id
        self.start_time = datetime.now()
        self.responses = []
        self.completed = False

    def record_response(
        self,
        question_id: str,
        correct: bool,
        response_time: float,
        confidence: float
    ):

        self.responses.append({
            "question_id": question_id,
            "correct": correct,
            "response_time": response_time,
            "confidence": confidence,
            "timestamp": datetime.now()
        })

    def finish(self):
        self.completed = True
        self.end_time = datetime.now()

    def get_summary(self):

        total = len(self.responses)
        correct = sum(1 for r in self.responses if r["correct"])

        avg_time = (
            sum(r["response_time"] for r in self.responses) / total
            if total > 0 else 0
        )

        avg_confidence = (
            sum(r["confidence"] for r in self.responses) / total
            if total > 0 else 0
        )

        return {
            "score": correct,
            "total": total,
            "accuracy": correct / total if total else 0,
            "avg_time": avg_time,
            "avg_confidence": avg_confidence
        }