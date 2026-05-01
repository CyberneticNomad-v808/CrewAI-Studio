# CrewAI Studio JSON Schema

Official JSON Schema and validation tools for CrewAI Studio crew configurations.

## Quick Start

```bash
# Validate your JSON file
python3 validate-crew-json.py your-crew.json

# View the schema
cat crewai-studio-schema.json
```

## Files

| File | Purpose |
|------|---------|
| `crewai-studio-schema.json` | Official JSON Schema (Draft 07) |
| `validate-crew-json.py` | Validation tool |
| `CREW_JSON_FORMAT.md` | Complete format specification |

## JSON Structure

A CrewAI Studio crew configuration includes:

- **Crew metadata** - ID, name, process type, settings
- **Tools** - Reusable tools available to agents
- **Agents** - AI agents with roles and capabilities
- **Tasks** - Work items assigned to agents

### Minimal Example

```json
{
  "id": "C_my_crew",
  "name": "My Crew",
  "process": "sequential",
  "verbose": true,
  "memory": false,
  "cache": true,
  "planning": false,
  "planning_llm": null,
  "max_rpm": 1000,
  "manager_llm": null,
  "manager_agent": null,
  "created_at": "2025-10-12T00:00:00.000000",
  "tools": [],
  "agents": [],
  "tasks": []
}
```

## Key Requirements

### ID Patterns

All IDs must follow specific patterns:

```
Tools:  tool_[name]    → tool_file_read
Agents: agent_[name]   → agent_python_developer
Tasks:  task_[name]    → task_implement_feature
```

### Required Fields

**Tool:**
- `tool_id`, `name`, `description`, `parameters`

**Agent:**
- `id`, `role`, `goal`, `backstory`, `verbose`, `allow_delegation`
- `cache`, `llm_provider_model`, `temperature`, `max_iter`, `tool_ids`

**Task:**
- `id`, `description`, `expected_output`, `async_execution`, `agent_id`
- `context_from_async_tasks_ids`, `context_from_sync_tasks_ids`, `created_at`

### LLM Formats

```
Ollama:    "ollama/llama3.1:70b"
OpenAI:    "OpenAI: gpt-4"
Groq:      "Groq: llama-3.1-70b-versatile"
Anthropic: "Anthropic: claude-3-opus-20240229"
```

## Validation

```bash
python3 validate-crew-json.py your-crew.json
```

### Success

```
✅ VALIDATION PASSED!

📊 Summary:
  - Crew ID: C_my_crew
  - Crew Name: My Crew
  - Process: sequential
  - Tools: 5
  - Agents: 3
  - Tasks: 10
```

### Failure

```
❌ VALIDATION FAILED!

Error at: agents -> 0
Message: 'llm_provider_model' is a required property
```

## Documentation

See `CREW_JSON_FORMAT.md` for:
- Complete field specifications
- Detailed examples
- Naming conventions
- Best practices

## Examples

Working examples are available:
- `crewai-migration-crew-atomic-fixed.json` (60 tasks)
- `crewai-migration-crew-fixed.json` (445 tasks)

## Installation

```bash
# Install validation dependency
pip install jsonschema

# Make validator executable
chmod +x validate-crew-json.py
```

## Schema Version

**Version:** 1.0
**Standard:** JSON Schema Draft 07
**Updated:** 2025-10-12

---

For detailed format specification, see **CREW_JSON_FORMAT.md**
