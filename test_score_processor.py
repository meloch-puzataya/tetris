import pytest
import os
import tempfile
from score_processor import ScoreProcessor


@pytest.fixture
def temp_score_file():
    """Create a temporary score file for testing."""
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test_score.txt")

    processor = ScoreProcessor()
    processor.filepath = temp_file

    yield processor, temp_file

    # Cleanup
    if os.path.exists(temp_file):
        os.remove(temp_file)
    os.rmdir(temp_dir)


# test ScoreProcessor singleton pattern


def test_singleton_instance():
    processor1 = ScoreProcessor()
    processor2 = ScoreProcessor()
    assert processor1 is processor2


# test ScoreProcessor.get_score method


def test_get_score_file_not_exists(temp_score_file):
    processor, _ = temp_score_file
    score = processor.get_score()
    assert score == 0


def test_get_score_from_valid_file(temp_score_file):
    processor, temp_file = temp_score_file
    with open(temp_file, "w") as f:
        f.write("150")

    score = processor.get_score()
    assert score == 150


def test_get_score_invalid_content_not_digit(temp_score_file):
    processor, temp_file = temp_score_file
    with open(temp_file, "w") as f:
        f.write("invalid")

    score = processor.get_score()
    assert score == 0


def test_get_score_empty_file(temp_score_file):
    processor, temp_file = temp_score_file
    open(temp_file, "w").close()

    score = processor.get_score()
    assert score == 0


# test ScoreProcessor.save_score method


def test_save_score_creates_file(temp_score_file):
    processor, temp_file = temp_score_file
    # Ensure file doesn't exist
    if os.path.exists(temp_file):
        os.remove(temp_file)

    processor.save_score(100)
    assert os.path.exists(temp_file)


def test_save_score_writes_correct_value(temp_score_file):
    processor, temp_file = temp_score_file
    processor.save_score(250)

    with open(temp_file, "r") as f:
        content = f.read()

    assert content == "250"


def test_save_score_overwrites_previous(temp_score_file):
    processor, temp_file = temp_score_file
    processor.save_score(100)
    processor.save_score(200)

    with open(temp_file, "r") as f:
        content = f.read()

    assert content == "200"
