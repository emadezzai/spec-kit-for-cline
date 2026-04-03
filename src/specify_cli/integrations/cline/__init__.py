"""Cline integration."""

from pathlib import Path
from typing import Any

from ..base import MarkdownIntegration
from ..manifest import IntegrationManifest


class ClineIntegration(MarkdownIntegration):
    key = "cline"
    config = {
        "name": "Cline",
        "folder": ".clinerules/",
        "commands_subdir": "workflows",
        "install_url": "https://docs.cline.bot/getting-started/installing-cline",
        "requires_cli": False,
    }
    registrar_config = {
        "dir": ".clinerules/workflows",
        "format": "markdown",
        "args": "$ARGUMENTS",
        "extension": ".md",
    }
    context_file = ".clinerules/specify-rules.md"

    _INITIAL_RULES = """# Spec Kit Cline Rules

Use the workflows in `.clinerules/workflows/` as the primary entrypoints for the Spec Kit process.

- Start with `speckit.constitution` to set project principles.
- Continue with `speckit.specify`, `speckit.plan`, and `speckit.tasks` in order.
- After a plan exists, run the generated update-context script to refresh this file with project-specific guidance.
"""

    def setup(
        self,
        project_root: Path,
        manifest: IntegrationManifest,
        parsed_options: dict[str, Any] | None = None,
        **opts: Any,
    ) -> list[Path]:
        created = super().setup(project_root, manifest, parsed_options, **opts)

        rules_file = project_root / ".clinerules" / "specify-rules.md"
        if not rules_file.exists():
            created.append(
                self.write_file_and_record(
                    self._INITIAL_RULES,
                    rules_file,
                    project_root,
                    manifest,
                )
            )

        return created
