# CrewAI Studio JSON Format Specification

Official JSON format specification for CrewAI Studio crew configurations.

**Version:** 1.0
**Schema:** `crewai-studio-schema.json` (JSON Schema Draft 07)

---

## Validation

```bash
python3 validate-crew-json.py your-crew.json
```

---

## Structure Overview

```json
{
  "id": "crew_unique_id",
  "name": "Crew Name",
  "process": "sequential" | "hierarchical",
  "verbose": true,
  "memory": true,
  "cache": true,
  "planning": false,
  "planning_llm": "ollama/llama3.1:70b",
  "max_rpm": 1000,
  "manager_llm": "ollama/llama3.1:70b",
  "manager_agent": "agent_manager_id",
  "created_at": "2025-10-12T00:00:00.000000",
  "agents": [ ],
  "tasks": [ ],
  "tools": [ ]
}
```

---

## Tools

### Format

```json
{
  "tool_id": "tool_unique_identifier",
  "name": "ToolClassName",
  "description": "Description of what the tool does",
  "parameters": {
    "param1": "value1"
  }
}
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `tool_id` | string | Pattern: `^tool_[A-Za-z0-9_-]+$` |
| `name` | string | Tool class name from TOOL_CLASSES |
| `description` | string | Human-readable description |
| `parameters` | object | Tool configuration (can be `{}`) |

### Example

```json
{
  "tool_id": "tool_file_read",
  "name": "FileReadTool",
  "description": "Read contents of a file from the filesystem",
  "parameters": {}
}
```

---

## Agents

### Format

```json
{
  "id": "agent_unique_identifier",
  "role": "Agent Role",
  "goal": "Agent's primary objective",
  "backstory": "Agent's background and expertise",
  "verbose": true,
  "allow_delegation": true,
  "cache": true,
  "llm_provider_model": "ollama/llama3.1:70b",
  "temperature": 0.7,
  "max_iter": 25,
  "tool_ids": ["tool_id1", "tool_id2"],
  "created_at": "2025-10-12T00:00:00.000000"
}
```

### Required Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `id` | string | - | Pattern: `^agent_[A-Za-z0-9_-]+$` |
| `role` | string | - | Agent's role or title |
| `goal` | string | - | Primary objective |
| `backstory` | string | - | Background and expertise |
| `verbose` | boolean | - | Enable verbose output |
| `allow_delegation` | boolean | - | Can delegate to other agents |
| `cache` | boolean | `true` | Enable caching |
| `llm_provider_model` | string | - | LLM specification (see below) |
| `temperature` | number | `0.7` | Range: 0.0 - 2.0 |
| `max_iter` | integer | `25` | Maximum iterations |
| `tool_ids` | array | - | Array of tool IDs |
| `created_at` | string | - | ISO 8601 timestamp |

### LLM Provider Formats

```
Ollama:    "ollama/model:tag"              → "ollama/llama3.1:70b"
OpenAI:    "OpenAI: model-name"            → "OpenAI: gpt-4"
Groq:      "Groq: model-name"              → "Groq: llama-3.1-70b-versatile"
Anthropic: "Anthropic: model-name"         → "Anthropic: claude-3-opus-20240229"
```

### Example

```json
{
  "id": "agent_python_developer",
  "role": "Python Developer",
  "goal": "Write clean, idiomatic Python code following best practices",
  "backstory": "Expert Python developer with deep knowledge of modern Python patterns",
  "verbose": true,
  "allow_delegation": false,
  "cache": true,
  "llm_provider_model": "ollama/llama3.1:70b",
  "temperature": 0.7,
  "max_iter": 25,
  "tool_ids": ["tool_file_read", "tool_file_write"],
  "created_at": "2025-10-12T00:00:00.000000"
}
```

---

## Tasks

### Format

```json
{
  "id": "task_unique_identifier",
  "description": "Detailed task description with objectives",
  "expected_output": "Description of expected deliverable",
  "async_execution": false,
  "agent_id": "agent_unique_identifier",
  "context_from_async_tasks_ids": null,
  "context_from_sync_tasks_ids": ["task_id1"],
  "created_at": "2025-10-12T00:00:00.000000"
}
```

### Required Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `id` | string | - | Pattern: `^task_[A-Za-z0-9_-]+$` |
| `description` | string | - | Detailed task description |
| `expected_output` | string | - | Expected deliverable |
| `async_execution` | boolean | `false` | Execute in parallel |
| `agent_id` | string | - | Assigned agent ID |
| `context_from_async_tasks_ids` | array\|null | `null` | Async task dependencies |
| `context_from_sync_tasks_ids` | array\|null | `null` | Sync task dependencies |
| `created_at` | string | - | ISO 8601 timestamp |

### Task Dependencies

Use context fields to create task dependencies:

```json
{
  "id": "task_implementation",
  "agent_id": "agent_developer",
  "context_from_sync_tasks_ids": ["task_design", "task_planning"],
  "context_from_async_tasks_ids": null
}
```

### Example

```json
{
  "id": "task_implement_authentication",
  "description": "Implement JWT-based authentication system with login and registration endpoints",
  "expected_output": "Working authentication system with unit tests and API documentation",
  "async_execution": false,
  "agent_id": "agent_python_developer",
  "context_from_async_tasks_ids": null,
  "context_from_sync_tasks_ids": ["task_design_api"],
  "created_at": "2025-10-12T00:00:00.000000"
}
```

---

## ID Naming Conventions

### Pattern Requirements

| Type | Pattern | Example |
|------|---------|---------|
| Tool | `^tool_[A-Za-z0-9_-]+$` | `tool_file_read` |
| Agent | `^agent_[A-Za-z0-9_-]+$` | `agent_python_developer` |
| Task | `^task_[A-Za-z0-9_-]+$` | `task_implement_auth` |

### Naming Best Practices

**Tools:** Describe functionality
- `tool_file_read`, `tool_api_client`, `tool_code_executor`

**Agents:** Describe role
- `agent_python_developer`, `agent_test_engineer`, `agent_architect`

**Tasks:** Describe action or sequence
- `task_implement_feature`, `task_1_2_impl`, `task_final_review`

---

## Process Types

### Sequential
Tasks execute one after another in order.

```json
{
  "process": "sequential",
  "manager_llm": null,
  "manager_agent": null
}
```

### Hierarchical
Manager agent coordinates task execution.

```json
{
  "process": "hierarchical",
  "manager_llm": "ollama/llama3.1:70b",
  "manager_agent": "agent_program_manager"
}
```

Use either `manager_llm` (string) or `manager_agent` (agent ID), not both.

---

## Complete Example

```json
{
  "id": "C_example_crew",
  "name": "Example Development Crew",
  "process": "sequential",
  "verbose": true,
  "memory": true,
  "cache": true,
  "planning": false,
  "planning_llm": null,
  "max_rpm": 1000,
  "manager_llm": null,
  "manager_agent": null,
  "created_at": "2025-10-12T00:00:00.000000",
  "tools": [
    {
      "tool_id": "tool_file_read",
      "name": "FileReadTool",
      "description": "Read file contents",
      "parameters": {}
    }
  ],
  "agents": [
    {
      "id": "agent_developer",
      "role": "Python Developer",
      "goal": "Write quality Python code",
      "backstory": "Experienced Python developer",
      "verbose": true,
      "allow_delegation": false,
      "cache": true,
      "llm_provider_model": "ollama/llama3.1:70b",
      "temperature": 0.7,
      "max_iter": 25,
      "tool_ids": ["tool_file_read"],
      "created_at": "2025-10-12T00:00:00.000000"
    }
  ],
  "tasks": [
    {
      "id": "task_implement",
      "description": "Implement the feature",
      "expected_output": "Working implementation",
      "async_execution": false,
      "agent_id": "agent_developer",
      "context_from_async_tasks_ids": null,
      "context_from_sync_tasks_ids": null,
      "created_at": "2025-10-12T00:00:00.000000"
    }
  ]
}
```

---

## Validation

### Command
```bash
python3 validate-crew-json.py your-crew.json
```

### Success Output
```
✅ VALIDATION PASSED!

📊 Summary:
  - Crew ID: C_example_crew
  - Crew Name: Example Development Crew
  - Process: sequential
  - Tools: 1
  - Agents: 1
  - Tasks: 1
```

### Failure Output
```
❌ VALIDATION FAILED!

Error at: agents -> 0
Message: 'llm_provider_model' is a required property
```

---

## Schema Reference

The complete JSON Schema is available in `crewai-studio-schema.json`.

This schema follows JSON Schema Draft 07 and can be used with any JSON Schema validator.

---

## Working Examples

- `crewai-migration-crew-atomic-fixed.json` - Small crew (60 tasks)
- `crewai-migration-crew-fixed.json` - Large crew (445 tasks)

---

**Version:** 1.0
**Last Updated:** 2025-10-12
**Schema File:** `crewai-studio-schema.json`
