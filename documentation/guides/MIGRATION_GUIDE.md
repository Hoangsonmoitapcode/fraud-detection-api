# Database Migration Guide

## Overview
This project uses **Alembic** for database migrations. You can add/modify columns without losing data!

## Quick Commands

### Check current migration status:
```bash
.venv\Scripts\python.exe -m alembic current
```

### View migration history:
```bash
.venv\Scripts\python.exe -m alembic history --verbose
```

### Create a new migration (after changing models):
```bash
.venv\Scripts\python.exe -m alembic revision --autogenerate -m "Your migration message"
```

### Apply migrations:
```bash
.venv\Scripts\python.exe -m alembic upgrade head
```

### Rollback to previous migration:
```bash
.venv\Scripts\python.exe -m alembic downgrade -1
```

## Step-by-Step: Adding a New Column

### 1. Modify your model (src/models.py):
```python
class User(Base):
    # ... existing fields ...
    new_field = Column(String, nullable=True)  # Add your new field
```

### 2. Create migration:
```bash
.venv\Scripts\python.exe -m alembic revision --autogenerate -m "Add new_field column"
```

### 3. Review the generated migration file in `alembic/versions/`

### 4. Apply the migration:
```bash
.venv\Scripts\python.exe -m alembic upgrade head
```

### 5. Your database now has the new column without losing data! 🎉

## Common Migration Commands

| Command | Description |
|---------|-------------|
| `alembic current` | Show current migration |
| `alembic history` | Show all migrations |
| `alembic upgrade head` | Apply all pending migrations |
| `alembic downgrade -1` | Rollback one migration |
| `alembic downgrade base` | Rollback all migrations |
| `alembic stamp head` | Mark database as up-to-date |

## Migration Best Practices

1. **Always review** generated migration files before applying
2. **Test migrations** on a copy of your data first
3. **Backup your database** before major migrations
4. **Use descriptive messages** for your migrations
5. **Don't edit** applied migration files

## Troubleshooting

### If you get "No such revision" error:
```bash
.venv\Scripts\python.exe -m alembic stamp head
```

### If you need to reset everything:
```bash
.venv\Scripts\python.exe manage_db.py reset
.venv\Scripts\python.exe -m alembic stamp head
```

## Example: Your Recent Migration
We just added a `created_at` column using:
1. Modified `src/models.py` to add the field
2. Created migration: `alembic revision --autogenerate -m "Add created_at column"`  
3. Applied migration: `alembic upgrade head`
4. ✅ Column added without losing existing data!
