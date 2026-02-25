class EventBus:

    @staticmethod
    def push_teacher_update(class_id, payload):
        """
        Replace with WebSocket / Redis pub-sub later.
        """
        print(f"[Teacher Update] Class {class_id}")
        print(payload)