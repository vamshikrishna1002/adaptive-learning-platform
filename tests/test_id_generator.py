# tests/test_id_generator.py

from src.id_generator import generate_id

def test_generate_learner_id():
    assert generate_id("LRN", 1) == "LRN-000001"
    

