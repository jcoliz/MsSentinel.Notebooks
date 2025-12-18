# Notebook Templates

This directory contains templates for creating new notebooks with consistent structure and documentation.

## Templates

### notebook-template.ipynb
**AI-Assisted Notebook Development Template**

A starter template designed for creating Microsoft Sentinel notebooks using an AI assistant. This template provides:

- **Reference Documentation Links**: Essential Microsoft Sentinel and Azure documentation
- **Structured Workflow**: Three-phase approach (Design → Plan → Implement)
- **Task Description Area**: Space to describe what the notebook should accomplish
- **Best Practices**: Tips for effective AI collaboration
- **Example Prompts**: Ready-to-use prompts for each phase

**Usage:**
1. Copy [`notebook-template.ipynb`](notebook-template.ipynb) to your workspace directory
2. Describe your analysis task in the first cell
3. Share the reference links with your AI assistant
4. Follow the three-phase workflow:
   - Phase 1: Create design document (iterate until satisfied)
   - Phase 2: Create implementation plan (iterate until satisfied)
   - Phase 3: Build notebook cell-by-cell (test each cell before moving on)

**Philosophy:**
This template embraces AI-assisted development where users describe their security analysis goals in natural language, and an AI assistant helps design and implement the solution. The iterative approach ensures each component works correctly before proceeding.

### README-template.md
Template for notebook README files (user-facing overview).

### DESIGN-template.md
Template for design documentation (architecture and approach).

### IMPLEMENTATION-template.md
Template for implementation documentation (technical details).

## AI-Assisted Development Workflow

The [`notebook-template.ipynb`](notebook-template.ipynb) implements a collaborative workflow:

### Phase 1: Design 📋
Ask your AI: *"Create a detailed design document for this notebook."*
- Review data sources and table schemas
- Validate analysis methodology
- Confirm output schema
- Iterate until the design meets your needs
- Save final design as `DESIGN.md`

### Phase 2: Implementation Plan 🗺️
Ask your AI: *"Create a step-by-step implementation plan."*
- Review logical flow and structure
- Validate required libraries and imports
- Confirm error handling strategies
- Iterate to match your environment
- Save final plan as `IMPLEMENTATION.md`

### Phase 3: Implementation 💻
Ask your AI: *"Create the first cell according to the plan."*
- Test each cell immediately
- Share errors and iterate until it works
- Validate data quality at each step
- Move to next cell only when current cell works
- Repeat until notebook is complete

## Traditional Development

For manual notebook development, use the documentation templates:

1. **README.md**: Update with notebook-specific overview, prerequisites, and usage
2. **DESIGN.md**: Document the architecture, data sources, and analytical approach
3. **IMPLEMENTATION.md**: Add implementation notes, known issues, and improvement ideas
4. **notebook.ipynb**: Implement your notebook logic with clear markdown explanations

## Template Structure

Each template includes:
- Placeholder sections to guide content creation
- Examples of what to include
- Consistent formatting and structure
- Links to related documentation

---

**Get Started:** Copy [`notebook-template.ipynb`](notebook-template.ipynb) and begin your AI-assisted notebook development!
