from mole_ai.cli import main


def test_cli_version(capsys, monkeypatch):

    monkeypatch.setattr(
        "sys.argv",
        ["mole_ai", "--version"],
    )

    main()

    captured = capsys.readouterr()

    assert "MOLE-AI Version 1.0" in captured.out
