from mole_ai.models.generation import (
    validate_smiles,
    generate_candidate_smiles,
)


def test_validate_valid_smiles():

    smiles = "CCO"

    result = validate_smiles(
        smiles
    )

    assert result is True


def test_validate_invalid_smiles():

    smiles = "INVALID"

    result = validate_smiles(
        smiles
    )

    assert result is False


def test_generate_candidate_smiles():

    seed = "CCO"

    generated = generate_candidate_smiles(
        seed
    )

    assert isinstance(
        generated,
        str,
    )

    assert validate_smiles(
        generated
    ) is True


def test_invalid_generation():

    try:
        generate_candidate_smiles(
            "INVALID"
        )

        assert False

    except ValueError:

        assert True
