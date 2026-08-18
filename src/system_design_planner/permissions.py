from deepagents import FilesystemPermission

DESIGN_SESSION_PERMISSIONS = [
    # Secrets: never readable or writable by the agent, full stop.
    FilesystemPermission(operations=["read", "write"], paths=["/.env"], mode="deny"),

    # Reference corpus: read-only ground truth. The agent must never overwrite it.
    FilesystemPermission(operations=["write"], paths=["/knowledge_base/**"], mode="deny"),
    
    # Persistent memory: the one write that should never happen silently - a
    # human must approve before a scoping decision becomes permanent.
    FilesystemPermission(operations=["write"], paths=["/memory/AGENTS.md"], mode="interrupt"),
]
