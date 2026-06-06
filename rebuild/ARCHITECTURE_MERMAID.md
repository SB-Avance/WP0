# Arquitectura - Diagrama Mermaid

```mermaid
flowchart LR
  subgraph App[Rebuild FastAPI Service]
    direction TB
    Main[whatsapp_manager.main\n(FastAPI)]
    Config[core.config\n(Settings)]
    API[api/*\n(webhook, conversations, messages)]
    Static[static/dashboard.html]
    Tests[tests/*]
  end

  subgraph Services[Services]
    Dataverse[services.dataverse\n(DataverseClient)]
    WhatsApp[services.whatsapp\n(WhatsAppClient)]
    Mocks[services.mocks\n(MockClients)]
  end

  subgraph LocalDev[Local Dev & Scripts]
    RunLocal[run_local.ps1]
    Env[.env / .env.example]
    Dashboard[Dashboard UI]
  end

  subgraph Legacy[Archive / Legacy Code]
    LegacyBackend[archive/legacy/backend/*]
    LegacyHandlers[archive/legacy/handlers/*]
    Mobile[archive/legacy/mobile/*]
    Unused[archive/unused_root/*]
  end

  Main --> API
  Main --> Static
  Main --> Config
  API --> Dataverse
  API --> WhatsApp
  API --> Mocks
  Config --> Dataverse
  Config --> WhatsApp
  Mocks -. used in .env=LOCAL .-> API
  RunLocal --> Env
  RunLocal --> Main
  Dashboard --> API
  Tests --> API
  Tests --> Mocks

  LegacyBackend -. duplicado/antiguo .-> API
  LegacyHandlers -. business logic histórico .-> API
  Mobile -. client UI antiguo .-> Dashboard
  Unused -. utilidades/migraciones .-> Dataverse

  style App fill:#f9f,stroke:#333,stroke-width:1px
  style Services fill:#fffbcc,stroke:#333
  style LocalDev fill:#ccf2ff,stroke:#333
  style Legacy fill:#f2dede,stroke:#333

```
