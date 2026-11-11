import pytest

from services.chunking import chunk_text

def test_empty_text_returns_empty_list():
    assert chunk_text("") == []
    assert chunk_text("   ") == []

def test_short_text_is_single_chunk():
    assert chunk_text("hello world") == ["hello world"]

def test_basic_split_without_overlap():
    assert chunk_text("abcde", chunk_size=2, overlap=0) == ["ab", "cd", "e"]

def test_overlap_repeats_boundart_characters():
    # size=4, overlap=1 -> step=3, so 'd' ends the first chunk
    # and starts the second.
    assert chunk_text("abcdef", chunk_size=4, overlap=1) == ["abcd", "def"]

def test_long_text_chunk_count_and_overlap():
    text = "".join(chr(97 + i % 26) for i in range(1200))
    chunks = chunk_text(text, chunk_size=500, overlap=50)
    assert [len(c) for c in chunks] == [500, 500, 300]
    # the last 50 chars of a chunk reappear at the start of the next
    assert chunks[0][-50:] == chunks[1][:50]

@pytest.mark.parametrize(
    "kwargs",
    [{"chunk_size":0},
     {"chunk_size":5, "overlap": 5},
     {"chunk_size": 5, "overlap": -1},
     ],
)
def test_invalid_parameters_raise_value_error(kwargs):
    with pytest.raises(ValueError):
        chunk_text("x" * 10, **kwargs)