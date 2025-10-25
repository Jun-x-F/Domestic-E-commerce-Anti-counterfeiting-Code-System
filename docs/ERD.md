# Database ERD

```mermaid
erDiagram
    spu_channel_code {
        int id PK
        varchar spu
        varchar channel
        varchar code
        varchar url
        varchar qr_path
        datetime created_at
        datetime updated_at
    }
```
