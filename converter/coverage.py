CORE_FIELDS = (
    "run_id", "nodes", "edges", "observed_date", "status",
    "A01", "A02", "A03", "A04", "A05",
)
V1_0_EXCLUDED_VALIDATIONS = {
    "COND-101": "run uniqueness across files / multi-run merge",
    "COND-102": "isolated node",
    "COND-103": "cycle warn",
    "COND-104": "disconnected warn",
    "COND-105": "review must be sink",
}
GOLDEN_CASES = {
    "minimal": {"stem": "golden_minimal", "coverage": frozenset({"CORE_FIELDS"}), "validates_cond": frozenset()},
    "typical": {"stem": "golden", "coverage": frozenset({"CORE_FIELDS"}), "validates_cond": frozenset()},
    "sparse": {"stem": "golden_sparse", "coverage": frozenset({"CORE_FIELDS"}), "validates_cond": frozenset()},
    "extensions": {
        "stem": "golden_extensions",
        "coverage": frozenset({"CORE_FIELDS"}),
        "validates_cond": frozenset(),
        "pending_cond": frozenset({"COND-102", "COND-103", "COND-105"}),
    },
}
