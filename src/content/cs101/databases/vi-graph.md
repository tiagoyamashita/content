---
label: "VI"
subtitle: "Graph"
group: "Databases"
order: 6
---
Graph databases
A **graph** database stores **vertices** (nodes) and **edges** (relationships) with **properties** on both. Queries **traverse** the graph — follow friends, paths, cycles — instead of joining many SQL tables or pulling nested documents.

## 1. Data model

```text
(Ada:Person { born: 1815 })
    -[:KNOWS { since: 1833 }]-> (Charles:Person)
    -[:KNOWS]-> (Grace:Person)
(Grace)-[:WROTE]-> (Algorithm:Book { title: "..." })
```

| Piece | Meaning |
|-------|---------|
| **Vertex / node** | Entity (Person, Product, Account) |
| **Edge / relationship** | Typed link with direction (KNOWS, PURCHASED, FOLLOWS) |
| **Property** | Key-value on node or edge (`since: 1833`) |
| **Label** | Node type (`:Person`) |

**Property graph** model (Neo4j, Neptune) is most common in industry.

## 2. Graph vs relational JOINs

**SQL** — find friends of friends:

```sql
SELECT f2.name
FROM friends f1
JOIN friends f2 ON f1.friend_id = f2.user_id
WHERE f1.user_id = :me;
-- deeper hops → more JOINs or recursive CTE
```

**Cypher** (Neo4j):

```cypher
MATCH (me:Person {name: 'Ada'})-[:KNOWS*1..2]-(fof:Person)
RETURN DISTINCT fof.name;
```

The engine uses **index-free adjacency** — each node points to its edges — so **local traversal** is cheap. SQL can simulate graphs but **deep, variable-length path** queries get awkward at billion-edge scale.

## 3. Query languages

| Language | Used by |
|----------|---------|
| **Cypher** | Neo4j (declarative, pattern matching) |
| **Gremlin** | TinkerPop, Amazon Neptune (traversal steps) |
| **SPARQL** | RDF triple stores (semantic web) |
| **GQL** | Emerging ISO standard (Cypher-like) |

Gremlin flavor:

```text
g.V().has('Person', 'name', 'Ada')
  .out('KNOWS').out('KNOWS')
  .values('name')
```

## 4. Algorithms on graphs

Graph DBs shine when you need:

| Problem | Approach |
|---------|----------|
| **Shortest path** | BFS / Dijkstra on weighted edges |
| **Recommendations** | “Users who bought X also bought Y” — 2-hop patterns |
| **Fraud rings** | Detect dense subgraphs, shared attributes |
| **Access control** | Transitive “member of group” closure |
| **PageRank-style** | Importance via iterative traversal (often offline) |

CS101 **BFS/DFS** (`Algorithms` submenu) is the same idea on an in-memory adjacency list — the DB persists and indexes it.

## 5. Modeling tips

- **Model verbs as relationships**, not fake join tables when traversal is the main access (`(:User)-[:RATED {stars: 5}]->(:Movie)`).
- **Avoid supernodes** — one celebrity with 50M followers makes fan-out expensive; sometimes hybrid with key-value counts.
- **Duplicate** display properties on edges for read speed if updates are rare.

## 6. Strengths and limits

**Strengths**

- **Intuitive** for highly connected data
- **Fast multi-hop** queries vs deep SQL JOIN chains
- **Flexible schema** — new edge types without migrations hell
- **Visual exploration** in Neo4j Browser and similar tools

**Limits**

- **Global aggregations** (“sum all orders worldwide”) — SQL warehouses often better
- **Bulk analytics** — export to batch (Spark) rather than scan whole graph online
- **Sharding** graphs is hard — cuts break locality; managed services hide some pain
- **Smaller ecosystem** than PostgreSQL

## 7. When to choose graph

- Social networks, org charts, permission inheritance
- **Knowledge graphs** (entities linked by typed facts)
- **Fraud / AML** — pattern detection on accounts and transfers
- **Network / IT topology** — dependencies between services

Use **relational** when connections are simple FKs and reports dominate; use **graph** when **path queries** are the product core.

## 8. Examples

| Product | Notes |
|---------|--------|
| **Neo4j** | Native property graph, Cypher |
| **Amazon Neptune** | Gremlin + SPARQL, managed |
| **ArangoDB** | Multi-model (document + graph) |
| **PostgreSQL + recursive CTE** | Graph-like queries without separate DB |

## 9. Java sketch (Neo4j driver)

```java
// Compile: javac --release 22 …
try (var session = driver.session()) {
  session.run(
      "MATCH (p:Person {name: $name})-[:KNOWS]->(friend) RETURN friend.name",
      Values.parameters("name", "Ada")
  ).list(r -> r.get("friend.name").asString());
}
```

## 10. Related

- **Overview** — `i-overview.md`
- **Graph** (Data structures submenu) — adjacency list, BFS, DFS
- **Graph traversal** (Algorithms submenu) — algorithms the DB runs internally
- **Relational** — when JOINs suffice (`ii-relational.md`)
