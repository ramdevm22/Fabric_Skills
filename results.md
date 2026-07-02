# Fabric Skill Benchmark Results

### Using different frameworks

---
### Run: 2026-07-02 12:21 | Langchain | openai/gpt-4o-mini-2024-07-18
**Time:** 6.31s | **Correct:** YES

**Response:**

1. The exact `az rest` command to find all Lakehouses across your Microsoft Fabric workspaces is:

```bash
cat > /tmp/body.json << 'EOF'
{"search": "", "filter": "Type eq 'Lakehouse'", "pageSize": 1000}
EOF
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/catalog/search" \
  --body @/tmp/body.json
```

2. I chose Catalog Search because it allows for a single cross-workspace call to find items by type without needing to resolve each workspace individually.
| 2026-07-02 12:24 | LangChain + OpenRouter | openai/gpt-4o-mini-2024-07-18 | 5.36 | YES |

---
### Run: 2026-07-02 12:21 | Langchain | openai/gpt-4o-mini-2024-07-18
**Time:** 5.36s | **Correct:** YES

**Response:**

1. The exact `az rest` command to find all Lakehouses across your Microsoft Fabric workspaces is:

```bash
cat > /tmp/body.json << 'EOF'
{"search": "", "filter": "Type eq 'Lakehouse'", "pageSize": 1000}
EOF
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/catalog/search" \
  --body @/tmp/body.json
```

2. I chose Catalog Search because it allows for a single cross-workspace call to find items by type, rather than needing to resolve each workspace individually.
| 2026-07-02 12:25 | LangChain + OpenRouter | openai/gpt-4o-mini-2024-07-18 | 4.84 | YES |

---
### Run: 2026-07-02 12:21 | Langchain | openai/gpt-4o-mini-2024-07-18
**Time:** 4.84s | **Correct:** YES

**Response:**

1. The exact `az rest` command to find all Lakehouses across your Microsoft Fabric workspaces is:

```bash
cat > /tmp/body.json << 'EOF'
{"search": "", "filter": "Type eq 'Lakehouse'", "pageSize": 1000}
EOF
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/catalog/search" \
  --body @/tmp/body.json
```

2. I chose Catalog Search because it allows for a single cross-workspace call to find items by type without needing to resolve each workspace individually.
| 2026-07-02 12:25 | LangChain + OpenRouter | openai/gpt-4o-mini-2024-07-18 | 3.46 | YES |

---
### Run: 2026-07-02 12:21 | Langchain | openai/gpt-4o-mini-2024-07-18
**Time:** 3.46s | **Correct:** YES

**Response:**

1. The exact `az rest` command to find all Lakehouses across your Microsoft Fabric workspaces is:

```bash
cat > /tmp/body.json << 'EOF'
{"search": "", "filter": "Type eq 'Lakehouse'", "pageSize": 1000}
EOF
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/catalog/search" \
  --body @/tmp/body.json
```

2. I chose Catalog Search because it allows for a single cross-workspace call to find items by type without needing to resolve each workspace individually.
| 2026-07-02 12:26 | smolagents | openai/gpt-4o-mini-2024-07-18 | 9.31 | YES |

---
### Run: 2026-07-01 16:20 | smolagents | openai/gpt-4o-mini-2024-07-18
**Time:** 7.70s | **Correct:** YES

**Response:**

1. The exact `az rest` command to find all Lakehouses across workspaces is:
```bash
cat > /tmp/body.json << 'EOF'
{"search": "", "filter": "Type eq 'Lakehouse'", "pageSize": 1000}
EOF
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/catalog/search" \
  --body @/tmp/body.json
```

2. I chose Catalog Search instead of listing workspaces directly because the Catalog Search API allows for finding items across all workspaces in a single call, which is more efficient than resolving each workspace individually.
| 2026-07-01 16:54 | Google ADK | openai/gpt-4o-mini | 9.21 | YES |

### Run: 2026-07-02 12:26 | smolagents | openai/gpt-4o-mini-2024-07-18
**Time:** 9.31s | **Correct:** YES

**Response:**

1. The exact `az rest` command to find all Lakehouses across workspaces is:
```bash
cat > /tmp/body.json << 'EOF'
{"search": "", "filter": "Type eq 'Lakehouse'", "pageSize": 1000}
EOF
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/catalog/search" \
  --body @/tmp/body.json
```

2. I chose Catalog Search instead of listing workspaces directly because the Catalog Search API allows for a single cross-workspace call to find items, which is more efficient than resolving each workspace individually.
| 2026-07-02 12:28 | smolagents | openai/gpt-4o-mini-2024-07-18 | 7.23 | YES |

---
### Run: 2026-07-02 12:28 | smolagents | openai/gpt-4o-mini-2024-07-18
**Time:** 7.23s | **Correct:** YES

**Response:**

1. The exact `az rest` command to find all Lakehouses across workspaces is:
```bash
cat > /tmp/body.json << 'EOF'
{"search": "", "filter": "Type eq 'Lakehouse'", "pageSize": 1000}
EOF
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/catalog/search" \
  --body @/tmp/body.json
```

2. I chose Catalog Search instead of listing workspaces directly because the Catalog Search API allows for a single cross-workspace call to find items, which is more efficient than resolving each workspace individually.

---
### Run: 2026-07-01 16:54 | Google ADK | openai/gpt-4o-mini
**Time:** 9.21s | **Correct:** YES

**Response:**

1. The exact `az rest` command to find all Lakehouses across your Microsoft Fabric workspaces is:

```bash
cat > /tmp/body.json << 'EOF'
[["search": "", "filter": "Type eq 'Lakehouse'", "pageSize": 1000]]
EOF
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/catalog/search" \
  --body @/tmp/body.json
```

2. I chose Catalog Search because it allows for a single cross-workspace call that can find all Lakehouses without needing to resolve individual workspaces first.


---
### Run: 2026-07-02 12:30 | Google ADK | openai/gpt-4o-mini
**Time:** 7.56s | **Correct:** YES

**Response:**

1. The exact `az rest` command to find all Lakehouses across your Microsoft Fabric workspaces is:

```bash
cat > /tmp/body.json << 'EOF'
[["search": "", "filter": "Type eq 'Lakehouse'", "pageSize": 1000]]
EOF
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/catalog/search" \
  --body @/tmp/body.json
```

2. I chose Catalog Search instead of listing workspaces directly because the Catalog Search API allows for a single cross-workspace call to find all items of a specific type, such as Lakehouses, without needing to resolve each workspace individually.
| 2026-07-02 12:31 | Google ADK | openai/gpt-4o-mini | 8.77 | YES |

---
### Run: 2026-07-02 12:31 | Google ADK | openai/gpt-4o-mini
**Time:** 8.77s | **Correct:** YES

**Response:**

1. The exact `az rest` command to find all Lakehouses across your Microsoft Fabric workspaces is:

```bash
cat > /tmp/body.json << 'EOF'
[["search": "", "filter": "Type eq 'Lakehouse'", "pageSize": 1000]]
EOF
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/catalog/search" \
  --body @/tmp/body.json
```

2. I chose Catalog Search because it allows for a single cross-workspace call to retrieve all Lakehouses without needing to resolve each workspace individually.
| 2026-07-02 12:31 | Google ADK | openai/gpt-4o-mini | 7.10 | YES |

---
### Run: 2026-07-02 12:31 | Google ADK | openai/gpt-4o-mini
**Time:** 7.10s | **Correct:** YES

**Response:**

1. The exact `az rest` command to find all Lakehouses across your Microsoft Fabric workspaces is:

```bash
cat > /tmp/body.json << 'EOF'
[["search": "", "filter": "Type eq 'Lakehouse'", "pageSize": 1000]]
EOF
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/catalog/search" \
  --body @/tmp/body.json
```

2. I chose Catalog Search instead of listing workspaces directly because the Catalog Search API allows for a single cross-workspace call to find all items of a specific type without needing to resolve each workspace first.


| 2026-07-01 16:58 | AutoGen (Microsoft) | openai/gpt-4o-mini-2024-07-18 | 6.01 | YES |
---
### Run: 2026-07-01 16:58 | AutoGen | openai/gpt-4o-mini-2024-07-18
**Time:** 6.01s | **Correct:** YES

**Response:**

1. The exact `az rest` command to find all Lakehouses across your Microsoft Fabric workspaces is:

```bash
cat > /tmp/body.json << 'EOF'
{"search": "", "filter": "Type eq 'Lakehouse'", "pageSize": 1000}
EOF
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/catalog/search" \
  --body @/tmp/body.json
```

2. I chose Catalog Search because it allows for a single cross-workspace call to find items by type, rather than needing to resolve each workspace individually.
| 2026-07-02 12:17 | AutoGen (Microsoft) | openai/gpt-4o-mini-2024-07-18 | 5.54 | YES |

---
### Run: 2026-07-02 12:17 | AutoGen | openai/gpt-4o-mini-2024-07-18
**Time:** 5.54s | **Correct:** YES

**Response:**

1. The exact `az rest` command to find all Lakehouses across your Microsoft Fabric workspaces is:

```bash
cat > /tmp/body.json << 'EOF'
{"search": "", "filter": "Type eq 'Lakehouse'", "pageSize": 1000}
EOF
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/catalog/search" \
  --body @/tmp/body.json
```

2. I chose Catalog Search because it allows for a single cross-workspace call to find items by type without needing to resolve each workspace individually.
| 2026-07-02 12:18 | AutoGen (Microsoft) | openai/gpt-4o-mini-2024-07-18 | 4.80 | YES |

---
### Run: 2026-07-02 12:18 | AutoGen | openai/gpt-4o-mini-2024-07-18
**Time:** 4.80s | **Correct:** YES

**Response:**

1. The exact `az rest` command to find all Lakehouses across your Microsoft Fabric workspaces is:

```bash
cat > /tmp/body.json << 'EOF'
{"search": "", "filter": "Type eq 'Lakehouse'", "pageSize": 1000}
EOF
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/catalog/search" \
  --body @/tmp/body.json
```

2. I chose Catalog Search because it allows for a single cross-workspace call to find items by type, rather than needing to resolve each workspace individually.
| 2026-07-02 12:18 | AutoGen (Microsoft) | openai/gpt-4o-mini-2024-07-18 | 4.44 | YES |

---
### Run: 2026-07-02 12:18 | AutoGen | openai/gpt-4o-mini-2024-07-18
**Time:** 4.44s | **Correct:** YES

**Response:**

1. The exact `az rest` command to find all Lakehouses across your Microsoft Fabric workspaces is:

```bash
cat > /tmp/body.json << 'EOF'
{"search": "", "filter": "Type eq 'Lakehouse'", "pageSize": 1000}
EOF
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/catalog/search" \
  --body @/tmp/body.json
```

2. I chose Catalog Search because it allows for a single cross-workspace call to find items by type, rather than needing to resolve each workspace individually.
| 2026-07-02 12:19 | AutoGen (Microsoft) | openai/gpt-4o-mini-2024-07-18 | 6.34 | YES |

---
### Run: 2026-07-02 12:19 | AutoGen | openai/gpt-4o-mini-2024-07-18
**Time:** 6.34s | **Correct:** YES

**Response:**

1. The exact `az rest` command to find all Lakehouses across your Microsoft Fabric workspaces is:

```bash
cat > /tmp/body.json << 'EOF'
{"search": "", "filter": "Type eq 'Lakehouse'", "pageSize": 1000}
EOF
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/catalog/search" \
  --body @/tmp/body.json
```

2. I chose Catalog Search because it allows for a single cross-workspace call to find items by type, rather than needing to resolve each workspace individually.




### Using different models Using Langchain

| Timestamp | Framework | Model | Time (s) | Correct? |
|-----------|-----------|-------|----------|----------|
| 2026-07-01 12:46 | LangChain + OpenRouter | openai/gpt-oss-20b:free | 11.51 | YES |

---
### Run: 2026-07-01 12:46 | openai/gpt-oss-20b:free
**Time:** 11.51s | **Correct:** YES

**Response:**

**1. Command to list every Lakehouse in all workspaces**

```bash
cat > /tmp/body.json << 'EOF'
{"search": "", "filter": "Type eq 'Lakehouse'", "pageSize": 1000}
EOF

az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/catalog/search" \
  --body @/tmp/body.json
```

**2. Why Catalog Search is used instead of listing workspaces**

Catalog Search returns items across all workspaces in a single call and includes each item’s workspace information, whereas listing workspaces only gives workspace names and would require a separate call per workspace to discover the Lakehouses.
| 2026-07-01 14:01 | LangChain + OpenRouter | anthropic/claude-3-haiku | 3.88 | YES |

---
### Run: 2026-07-01 14:01 | anthropic/claude-3-haiku
**Time:** 3.88s | **Correct:** YES

**Response:**

1. To find all Lakehouses across your Microsoft Fabric workspaces, run the following command:

```bash
cat > /tmp/body.json << 'EOF'
{"search": "", "filter": "Type eq 'Lakehouse'", "pageSize": 1000}
EOF
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/catalog/search" \
  --body @/tmp/body.json
```

2. The skill document states that the Catalog Search API should be used instead of listing workspaces directly, as it "finds **items**, not workspaces", and the search text matches against item display name, description, and workspace name, which allows you to discover Lakehouses across workspaces without needing to know the workspace names.
| 2026-07-01 14:08 | LangChain + OpenRouter | openai/gpt-4o-mini-2024-07-18 | 5.89 | YES |

---
### Run: 2026-07-01 14:08 | openai/gpt-4o-mini-2024-07-18
**Time:** 5.89s | **Correct:** YES

**Response:**

1. The exact `az rest` command to find all Lakehouses across your Microsoft Fabric workspaces is:

```bash
cat > /tmp/body.json << 'EOF'
{"search": "", "filter": "Type eq 'Lakehouse'", "pageSize": 1000}
EOF
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/catalog/search" \
  --body @/tmp/body.json
```

2. I chose Catalog Search because it allows for a single cross-workspace call to find items by type, rather than needing to resolve each workspace individually.
| 2026-07-01 15:34 | LangChain + OpenRouter | google/gemini-2.5-flash-lite | 2.61 | YES |

---
### Run: 2026-07-01 15:34 | google/gemini-2.5-flash-lite
**Time:** 2.61s | **Correct:** YES

**Response:**

1. The exact `az rest` command (with body) I should run to do this:

```bash
cat > /tmp/body.json << 'EOF'
{"search": "", "filter": "Type eq 'Lakehouse'", "pageSize": 1000}
EOF
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/catalog/search" \
  --body @/tmp/body.json
```

2. I chose Catalog Search because it is a single cross-workspace call that finds items, whereas the Catalog Search API does not find workspaces directly.
| 2026-07-01 16:20 | smolagents | openai/gpt-4o-mini-2024-07-18 | 7.70 | YES |
