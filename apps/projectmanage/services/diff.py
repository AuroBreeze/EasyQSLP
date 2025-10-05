from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Any, Literal
import difflib

try:
    from diff_match_patch import diff_match_patch  # type: ignore
    HAS_DMP = True
except Exception:
    HAS_DMP = False


DiffMode = Literal['unified', 'html', 'dmp']


class DiffStrategy(ABC):
    @abstractmethod
    def diff(self, old: str, new: str) -> Dict[str, Any]:
        ...


class UnifiedDiffStrategy(DiffStrategy):
    def diff(self, old: str, new: str) -> Dict[str, Any]:
        old_lines = old.splitlines(keepends=True)
        new_lines = new.splitlines(keepends=True)
        patch = ''.join(
            difflib.unified_diff(old_lines, new_lines, fromfile='old', tofile='new')
        )
        return {
            'type': 'unified',
            'patch': patch,
        }


class HtmlDiffStrategy(DiffStrategy):
    def diff(self, old: str, new: str) -> Dict[str, Any]:
        html = difflib.HtmlDiff().make_table(
            old.splitlines(), new.splitlines(), context=True, numlines=2
        )
        return {
            'type': 'html',
            'html': html,
        }


class DMPDiffStrategy(DiffStrategy):
    def diff(self, old: str, new: str) -> Dict[str, Any]:
        if not HAS_DMP:
            # fallback to unified
            return UnifiedDiffStrategy().diff(old, new)
        dmp = diff_match_patch()
        diffs = dmp.diff_main(old, new)
        dmp.diff_cleanupSemantic(diffs)
        patches = dmp.patch_make(old, diffs)
        patch_text = dmp.patch_toText(patches)
        return {
            'type': 'dmp',
            'diffs': diffs,
            'patch': patch_text,
        }


class DiffService:
    def __init__(self, mode: DiffMode = 'unified') -> None:
        if mode == 'html':
            self.strategy: DiffStrategy = HtmlDiffStrategy()
        elif mode == 'dmp':
            self.strategy = DMPDiffStrategy()
        else:
            self.strategy = UnifiedDiffStrategy()

    def diff(self, old: str, new: str) -> Dict[str, Any]:
        return self.strategy.diff(old, new)
