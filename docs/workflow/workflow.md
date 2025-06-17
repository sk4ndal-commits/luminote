# 📚 Self-Learning Platform – User Workflow (Mermaid Flowchart)

:::mermaid
flowchart TD
    A[Login / Sign Up] --> B[Dashboard]

    B --> C{Resume Activity?}
    C -->|Yes| D[Continue Subject]
    C -->|No| E[Select / Create Subject]

    E --> F[Upload Materials or Exam]
    D --> G[View Subject Overview]

    F --> G
    G --> H[Read Study Material]
    G --> I[Practice Flashcards]
    G --> J[Ask AI Questions]

    H --> K[Generate Quiz]
    I --> K
    J --> K
    G --> K

    K --> L[Take Quiz / Exam]
    L --> M[Get Feedback & Score]
    M --> N[Review Mistakes]
    N --> O[Regenerate Quiz on Weak Areas]

    O --> L

    M --> P[Track Progress]
    P --> B
:::