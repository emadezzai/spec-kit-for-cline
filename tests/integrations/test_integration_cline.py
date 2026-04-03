"""Tests for ClineIntegration."""

from specify_cli.integrations import get_integration
from specify_cli.integrations.manifest import IntegrationManifest

from .test_integration_base_markdown import MarkdownIntegrationTests


class TestClineIntegration(MarkdownIntegrationTests):
    KEY = "cline"
    FOLDER = ".clinerules/"
    COMMANDS_SUBDIR = "workflows"
    REGISTRAR_DIR = ".clinerules/workflows"
    CONTEXT_FILE = ".clinerules/specify-rules.md"

    def test_setup_creates_files(self, tmp_path):
        integration = get_integration(self.KEY)
        manifest = IntegrationManifest(self.KEY, tmp_path)
        created = integration.setup(tmp_path, manifest)
        assert len(created) > 0

        command_files = [f for f in created if f.parent.name == "workflows"]
        assert command_files
        for file_path in command_files:
            assert file_path.exists()
            assert file_path.name.startswith("speckit.")
            assert file_path.name.endswith(".md")

        rules_file = tmp_path / ".clinerules" / "specify-rules.md"
        assert rules_file in created
        assert rules_file.exists()

    def test_setup_writes_to_correct_directory(self, tmp_path):
        integration = get_integration(self.KEY)
        manifest = IntegrationManifest(self.KEY, tmp_path)
        created = integration.setup(tmp_path, manifest)

        workflows_dir = (tmp_path / self.REGISTRAR_DIR).resolve()
        rules_file = (tmp_path / ".clinerules" / "specify-rules.md").resolve()

        for file_path in created:
            resolved = file_path.resolve()
            if resolved == rules_file:
                continue
            if "scripts" in file_path.parts:
                continue
            assert resolved.parent == workflows_dir, (
                f"{file_path} is not under {workflows_dir}"
            )

    def test_setup_creates_initial_rules_file(self, tmp_path):
        integration = get_integration(self.KEY)
        manifest = IntegrationManifest(self.KEY, tmp_path)

        integration.setup(tmp_path, manifest)

        rules_file = tmp_path / ".clinerules" / "specify-rules.md"
        assert rules_file.exists()
        assert "Spec Kit" in rules_file.read_text(encoding="utf-8")

    def _expected_files(self, script_variant: str) -> list[str]:
        files = super()._expected_files(script_variant)
        files.append(".clinerules/specify-rules.md")
        return sorted(files)
