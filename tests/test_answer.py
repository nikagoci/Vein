from src.answer import check_citations, ask, REFUSAL
from src.retrieve import load_chunks

def test_invented_citation_refused():
    assert check_citations("Caesar shifts letters [9].", 2) == (False, "unknown citation")


def test_uncited_sentence_refused():
    assert check_citations("Caesar shifts letters [1]. It is old.", 2) == (False, "uncited sentence")


def test_low_score_refuses_without_calling_model(tmp_path):
    def boom(*a):
        raise AssertionError("model was called")
    r = ask("How do I hash passwords?", load_chunks(), generate=boom, log_path=tmp_path / 'u.jsonl')
    assert not r["grounded"] and r["answer"] == REFUSAL and r["reason"] == "below threshold"


def test_model_answer_with_bad_citation_refused(tmp_path):
    r = ask("How does the Caesar cipher work?", load_chunks(),
            generate=lambda q, h: "It shifts letters [7].", log_path=tmp_path / 'u.jsonl')
    assert not r["grounded"] and r["reason"] == "unknown citation"


def test_answer_maps_citation_to_right_document(tmp_path):
    r = ask("How does the Caesar cipher work?", load_chunks(), log_path=tmp_path / 'u.jsonl')
    assert r["grounded"] and r["citations"][0]["source"] == "caesar.md"
