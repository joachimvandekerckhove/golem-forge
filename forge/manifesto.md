# Golem Forge manifesto

Golem Forge is a way to specify my AI assistants as explicit, modular rule sets rather than as one-off prompts.

The core idea is simple:

> **Define small, orthogonal pieces (personalities, roles, domains) and compose them into Golems for specific tasks.**

This keeps my assistants:

- **Transparent** – I can see exactly which rules govern a given behavior.
- **Reproducible** – I can reuse the same Golem for different projects and know what I will get.
- **Composable** – I can mix and match pieces to create a new assistant without starting from scratch.

---

## Principles

### 1. Explicit over implicit

I do not rely on vibes or hidden state.  
Every behavioral constraint lives in a concrete file:

- Personality: how the Golem behaves.
- Role: what cognitive function it performs.
- Domain: what space it works in.

A Golem is just their product.

### 2. Orthogonality

Personalities, roles, and domains should overlap as little as possible:

- Personalities define *style and temperament*.
- Roles define *function*.
- Domains define *context and constraints*.

If I catch myself repeating the same rule across many files, I move it to a more global place.

### 3. Minimalism and discipline

Each `rules.md` file should be short and sharp:

- One page if possible, two at most.
- No wandering prose.
- No generic “be helpful” instructions.

The power comes from composition, not from bloated individual files.

### 4. Reuse across tools

I write rules in plain Markdown so I can use them:

- In Cursor as system prompts.
- In other chat interfaces.
- In documentation for collaborators.

I do not lock myself into one tool’s proprietary format.

### 5. Separation of concerns

I separate:

- **Behavioral rules** (this repo)  
  from
- **Project context** (paper specs, grant calls, syllabi living in their own repos).

A project prompt is:

> project-context + composed Golem prompt

This makes each piece easier to maintain.

---

## Design goals for Golems

A well-designed Golem:

1. **Knows its job**  
   The task is clear and bounded.

2. **Knows its style**  
   Its personality defines how it communicates and how aggressive or conservative it should be.

3. **Knows its context**  
   The domain tells it what counts as good work and what constraints to respect.

4. **Fails loudly**  
   When information is missing or assumptions are necessary, it flags them, it does not quietly improvise.

5. **Stays in its lane**  
   It does not drift into other roles or domains without being asked to.

---

## Naming and identity

Golems are named by their composition:

> **{Personality}–{Role} Golem of {Domain}**

For example:

- Rigorous Writer Golem of Manuscripts  
- Explainer Designer Golem of Teaching  
- Provocateur Reviewer Golem of Grants  

File slugs follow a simple convention:

- `rigorous-writer-manuscript.md`
- `explainer-designer-teaching.md`

---

## Future extensions

Possible extensions for Golem Forge:

- Meta-Golems that propose new personalities, roles, and domains.
- Project-specific Golems that include a fixed brief for a long-running project.
- Lightweight tagging of Golems with “aggressiveness”, “risk level”, or “strictness”.
- Simple tooling to pick personalities/roles/domains from a menu and assemble a prompt.

For now, the goal is to keep things simple and explicit:  
small Markdown files, a thin shell script, and compositional design.
