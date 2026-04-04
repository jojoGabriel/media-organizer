from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional


@dataclass
class FileRecord:
    path: str
    root_type: str
    category: str
    extension: str
    size_bytes: int
    modified_at: str
    sha256: Optional[str] = None
    duplicate_group: Optional[str] = None
    inferred_date: Optional[str] = None
    date_source: Optional[str] = None
    proposed_relative_destination: Optional[str] = None
    sidecar_for: Optional[str] = None
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


@dataclass
class ScanSummary:
    total_files: int = 0
    total_bytes: int = 0
    images: int = 0
    videos: int = 0
    sidecars: int = 0
    caches: int = 0
    unknown: int = 0
    duplicate_groups: int = 0
    duplicate_files: int = 0

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


@dataclass
class ScanReport:
    generated_at: str
    roots: Dict[str, str]
    summary: ScanSummary
    files: List[FileRecord]
    duplicate_groups: Dict[str, List[str]]

    def to_dict(self) -> Dict[str, object]:
        return {
            "generated_at": self.generated_at,
            "roots": self.roots,
            "summary": self.summary.to_dict(),
            "files": [file_record.to_dict() for file_record in self.files],
            "duplicate_groups": self.duplicate_groups,
        }

