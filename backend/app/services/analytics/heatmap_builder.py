from sqlalchemy.orm import Session
from app.models.mastery import Mastery


class HeatmapBuilder:

    @staticmethod
    def build_student_heatmap(db: Session):
        """
        Returns:
        {
            user_id: {
                concept: mastery_value
            }
        }
        """

        rows = db.query(Mastery).all()

        heatmap = {}

        for row in rows:
            if row.user_id not in heatmap:
                heatmap[row.user_id] = {}

            heatmap[row.user_id][row.concept] = row.mastery_value

        return heatmap


    @staticmethod
    def build_class_matrix(db: Session):
        """
        Returns:
        {
            "students": [list of ids],
            "concepts": [list of concepts],
            "matrix": [[values]]
        }
        """

        rows = db.query(Mastery).all()

        students = sorted(list(set(r.user_id for r in rows)))
        concepts = sorted(list(set(r.concept for r in rows)))

        matrix = []

        for student in students:
            row_values = []
            for concept in concepts:
                record = next(
                    (r for r in rows if r.user_id == student and r.concept == concept),
                    None
                )
                row_values.append(record.mastery_value if record else 0.0)

            matrix.append(row_values)

        return {
            "students": students,
            "concepts": concepts,
            "matrix": matrix
        }