SPEC_IDS = {"CORE-001","CORE-002","CORE-003","CORE-004","COND-101","COND-102","COND-103","COND-104","COND-105"}
EXCLUDED_CONDITIONS = {
    "COND-101": "cross-file run uniqueness",
    "COND-102": "orphan node detection",
    "COND-103": "cycle detection",
    "COND-104": "graph connectivity",
    "COND-105": "review sink validation",
}
SPEC_FIXTURES = {
    "COND-101": "fail_cond_101.yaml",
    "COND-102": "fail_cond_102.yaml",
    "COND-103": "fail_cond_103.yaml",
    "COND-104": "fail_cond_104.yaml",
    "COND-105": "fail_cond_105.yaml",
}
