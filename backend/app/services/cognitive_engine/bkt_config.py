from .mastery_update import BKTParameters

CONCEPT_PARAMS = {
    "algebra": BKTParameters(
        p_init=0.2,
        p_learn=0.15,
        p_guess=0.25,
        p_slip=0.1
    ),
    "probability": BKTParameters(
        p_init=0.25,
        p_learn=0.12,
        p_guess=0.2,
        p_slip=0.1
    ),
}
# TODO: Replace with DB-backed parameter loading in production