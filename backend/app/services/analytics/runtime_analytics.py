class RuntimeAnalytics:

    @staticmethod
    def compute_class_risk(class_states):
        if not class_states:
            return 0

        risks = []
        for state in class_states:
            avg_mastery = sum(state.mastery_dict.values()) / len(state.mastery_dict)
            risks.append(1 - avg_mastery)

        return sum(risks) / len(risks)


    @staticmethod
    def build_heatmap(class_states):
        return {
            state.user_id: state.mastery_dict
            for state in class_states
        }


    @staticmethod
    def generate_runtime_insights(student_state):
        weak = [
            c for c, m in student_state.mastery_dict.items()
            if m < 0.4
        ]

        return {
            "weak_topics": weak,
            "avg_mastery": sum(student_state.mastery_dict.values()) / len(student_state.mastery_dict)
        }