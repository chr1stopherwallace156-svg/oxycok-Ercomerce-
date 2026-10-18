"""Strict declarative boundary between the evidence and construction runtimes."""
import hashlib
import json

RELATIONS = {
    "NOT_EQUIVALENT", "DOES_NOT_IMPLY", "IMPLIES_UNDER_CONDITIONS",
    "EQUIVALENT_UNDER_CONDITIONS", "ANALOGOUS_UNDER_CONDITIONS", "CONTRADICTS",
}
RIGHTS = {
    "code_reuse": "PROHIBITED",
    "legal_clearance": "NOT_ESTABLISHED",
    "origin": "PROJECT_AUTHORED_ABSTRACTION",
}
MAX_BYTES = 1_000_000


class ContractError(ValueError):
    pass


def require(ok, reason):
    if not ok:
        raise ContractError(reason)


def exact(obj, keys):
    require(isinstance(obj, dict) and set(obj) == set(keys), "UNEXPECTED_CONTRACT_FIELDS")


def string(value):
    return isinstance(value, str) and 0 < len(value.strip()) <= 8192


def strings(value, required=False):
    return (isinstance(value, list) and len(value) <= 100
            and (bool(value) or not required) and all(string(x) for x in value)
            and len(value) == len(set(value)))


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def parse(raw):
    require(isinstance(raw, bytes) and len(raw) <= MAX_BYTES, "BRIEF_TOO_LARGE")
    def unique(pairs):
        out = {}
        for key, value in pairs:
            require(key not in out, "DUPLICATE_JSON_KEY")
            out[key] = value
        return out
    return validate(json.loads(raw, object_pairs_hook=unique))


def validate(brief):
    exact(brief, ["version", "kind", "authority", "action_authorized", "domain",
                  "facts", "facts_basis", "rights", "rules", "relations",
                  "evidence_pins", "coverage", "brief_sha256"])
    require(type(brief["version"]) is int and brief["version"] == 1, "INVALID_VERSION")
    require(brief["kind"] == "ABSTRACT_TRANSFER_BRIEF", "INVALID_KIND")
    require(brief["authority"] == "NONE" and brief["action_authorized"] is False,
            "AUTHORITY_ESCALATION")
    require(string(brief["domain"]) and strings(brief["facts"]), "INVALID_TASK")
    require(brief["facts_basis"] == "CALLER_DECLARED_NOT_INDEPENDENTLY_VERIFIED",
            "UNSUPPORTED_FACT_CLAIM")
    require(brief["rights"] == RIGHTS, "UNSUPPORTED_RIGHTS_OR_CODE_REUSE_CLAIM")
    require(brief["coverage"] == "BOUNDED_SEED_NOT_EXHAUSTIVE", "UNSUPPORTED_COVERAGE")
    require(isinstance(brief["rules"], list) and 0 < len(brief["rules"]) <= 100,
            "NO_CONSTRUCTIBLE_RULES")
    ids = set()
    for rule in brief["rules"]:
        exact(rule, ["id", "mechanism", "requires_all", "excludes_any", "principle",
                     "failure", "positive", "adapter", "test_obligations", "status"])
        require(string(rule["id"]) and rule["id"] not in ids, "DUPLICATE_RULE")
        ids.add(rule["id"])
        require(all(string(rule[x]) for x in
                    ["mechanism", "principle", "failure", "positive", "adapter"]),
                "INVALID_RULE_TEXT")
        require(strings(rule["requires_all"], True) and strings(rule["excludes_any"])
                and strings(rule["test_obligations"], True), "INVALID_RULE_CONDITIONS")
        require(not set(rule["requires_all"]) & set(rule["excludes_any"]),
                "CONTRADICTORY_CONDITIONS")
        require(rule["status"] == "TRANSFER_CANDIDATE", "UNSUPPORTED_PROMOTION")
    require(isinstance(brief["relations"], list) and len(brief["relations"]) <= 100,
            "INVALID_RELATIONS")
    relation_ids = set()
    for relation in brief["relations"]:
        exact(relation, ["id", "lesson_id", "left", "relation", "right", "conditions", "status"])
        require(string(relation["id"]) and relation["id"] not in relation_ids,
                "DUPLICATE_RELATION")
        relation_ids.add(relation["id"])
        require(relation["lesson_id"] in ids, "DANGLING_RELATION")
        require(string(relation["left"]) and string(relation["right"])
                and relation["left"] != relation["right"], "INVALID_RELATION_OPERANDS")
        require(isinstance(relation["relation"], str) and relation["relation"] in RELATIONS,
                "UNKNOWN_RELATION_TYPE")
        require(strings(relation["conditions"], True), "UNSCOPED_RELATION")
        require(relation["status"] == "CANDIDATE", "UNSUPPORTED_RELATION_PROOF")
    require(isinstance(brief["evidence_pins"], list) and brief["evidence_pins"],
            "MISSING_EVIDENCE_PINS")
    pin_ids = set()
    for pin in brief["evidence_pins"]:
        exact(pin, ["id", "repository", "commit", "path", "git_blob_sha"])
        require(all(string(x) for x in pin.values()), "INVALID_EVIDENCE_PIN")
        require(pin["id"] not in pin_ids, "DUPLICATE_EVIDENCE_PIN")
        pin_ids.add(pin["id"])
        require(all(len(pin[key]) == 40 and all(c in "0123456789abcdef" for c in pin[key])
                    for key in ("commit", "git_blob_sha")), "UNPINNED_EVIDENCE")
    unsigned = {k: v for k, v in brief.items() if k != "brief_sha256"}
    require(brief["brief_sha256"] == digest(unsigned), "BRIEF_HASH_MISMATCH")
    return brief
