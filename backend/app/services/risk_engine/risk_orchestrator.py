class RiskOrchestrator:
    def __init__(self, feature_extractor, predictor):
        self.feature_extractor = feature_extractor
        self.predictor = predictor

    def compute_risk(self, student_state, concept_graph):
        features = self.feature_extractor.extract(student_state, concept_graph)
        return self.predictor.predict(features)