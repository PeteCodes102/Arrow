#!/usr/bin/env python3
import argparse
from pathlib import Path
import re
from textwrap import dedent

def to_pascal(name: str) -> str:
    parts = re.split(r"[_\-\s]+", name.strip())
    return "".join(p.capitalize() for p in parts if p)

def write_file(path: Path, content: str, force: bool):
    if path.exists() and not force:
        print(f"SKIP  {path} (exists; use --force to overwrite)")
        return
    path.write_text(content, encoding="utf-8")
    print(f"WRITE {path}")

def main():
    parser = argparse.ArgumentParser(
        description="Generate a FastAPI module skeleton (router, schemas, service, repository)."
    )
    parser.add_argument("dir", help="Base directory to create the module in (will be created if needed).")
    parser.add_argument("name", help="Module name (e.g., 'data', 'user_profile').")
    parser.add_argument("--force", action="store_true", help="Overwrite files if they already exist.")
    parser.add_argument("--router", action="store_true", help="Include router file generation.")

    parser.add_argument()
    args = parser.parse_args()

    base_dir = Path(args.dir).expanduser().resolve()
    module_name = args.name.strip()
    pascal = to_pascal(module_name)

    module_dir = base_dir / module_name
    module_dir.mkdir(parents=True, exist_ok=True)

    # Files
    router_py = module_dir / "router.py"
    schemas_py = module_dir / "schemas.py"
    service_py = module_dir / "service.py"
    repository_py = module_dir / "repository.py"
    init_py = module_dir / "__init__.py"

    router_var = f"{module_name}_router"
    prefix = f"/{module_name}"

    router_code = dedent(f'''\
        from typing import List
        from fastapi import APIRouter, Depends, HTTPException, status

        from .schemas import {pascal}Create, {pascal}Read, {pascal}Update
        from .service import {pascal}Service, get_service

        {router_var} = APIRouter(prefix="{prefix}", tags=["{module_name}"])

        @{router_var}.get("/", response_model=List[{pascal}Read])
        def list_{module_name}(service: {pascal}Service = Depends(get_service)):
            """
            List {module_name} items.
            """
            return service.list()

        @{router_var}.get("/{{item_id}}", response_model={pascal}Read)
        def get_{module_name}(item_id: int, service: {pascal}Service = Depends(get_service)):
            """
            Get a single {module_name} item by ID.
            """
            item = service.get(item_id)
            if item is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="{pascal} not found")
            return item

        @{router_var}.post("/", response_model={pascal}Read, status_code=status.HTTP_201_CREATED)
        def create_{module_name}(payload: {pascal}Create, service: {pascal}Service = Depends(get_service)):
            """
            Create a new {module_name} item.
            """
            return service.create(payload)

        @{router_var}.put("/{{item_id}}", response_model={pascal}Read)
        def update_{module_name}(item_id: int, payload: {pascal}Update, service: {pascal}Service = Depends(get_service)):
            """
            Update an existing {module_name} item by ID.
            """
            updated = service.update(item_id, payload)
            if updated is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="{pascal} not found")
            return updated

        @{router_var}.delete("/{{item_id}}", status_code=status.HTTP_204_NO_CONTENT)
        def delete_{module_name}(item_id: int, service: {pascal}Service = Depends(get_service)):
            """
            Delete a {module_name} item by ID.
            """
            deleted = service.delete(item_id)
            if not deleted:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="{pascal} not found")
            return None
        ''')

    schemas_code = dedent(f'''\
        from pydantic import BaseModel, Field
        from typing import Optional

        class {pascal}Base(BaseModel):
            # Add your common fields here, e.g.:
            name: str = Field(..., description="Human-readable name")

        class {pascal}Create({pascal}Base):
            # Fields required only on create
            pass

        class {pascal}Update(BaseModel):
            # All fields optional for partial update
            name: Optional[str] = Field(None, description="Human-readable name")

        class {pascal}Read({pascal}Base):
            id: int = Field(..., description="Primary identifier")

            class Config:
                from_attributes = True  # pydantic v2 ORM mode
        ''')

    service_code = dedent(f'''\
        from typing import List, Optional
        from .schemas import {pascal}Create, {pascal}Read, {pascal}Update
        from .repository import {pascal}Repository

        class {pascal}Service:
            """
            Business logic layer for {module_name}.
            """
            def __init__(self, repo: {pascal}Repository):
                self.repo = repo

            def list(self) -> List[{pascal}Read]:
                return self.repo.list()

            def get(self, item_id: int) -> Optional[{pascal}Read]:
                return self.repo.get(item_id)

            def create(self, payload: {pascal}Create) -> {pascal}Read:
                return self.repo.create(payload)

            def update(self, item_id: int, payload: {pascal}Update) -> Optional[{pascal}Read]:
                return self.repo.update(item_id, payload)

            def delete(self, item_id: int) -> bool:
                return self.repo.delete(item_id)

        # Simple dependency that you can wire into FastAPI with Depends(...)
        def get_service() -> {pascal}Service:
            # Swap this out for DI container / db session wired repository
            repo = {pascal}Repository()
            return {pascal}Service(repo)
        ''')

    repository_code = dedent(f'''\
        from typing import List, Optional
        from itertools import count
        from .schemas import {pascal}Create, {pascal}Read, {pascal}Update

        class {pascal}Repository:
            """
            Data access layer for {module_name}.
            This in-memory implementation is for development; replace with a database-backed repo.
            """
            _ids = count(1)

            def __init__(self):
                self._items: dict[int, {pascal}Read] = {{}}

            def list(self) -> List[{pascal}Read]:
                return list(self._items.values())

            def get(self, item_id: int) -> Optional[{pascal}Read]:
                return self._items.get(item_id)

            def create(self, payload: {pascal}Create) -> {pascal}Read:
                new_id = next(self._ids)
                item = {pascal}Read(id=new_id, **payload.model_dump())
                self._items[new_id] = item
                return item

            def update(self, item_id: int, payload: {pascal}Update) -> Optional[{pascal}Read]:
                existing = self._items.get(item_id)
                if not existing:
                    return None
                data = existing.model_dump()
                data.update({{Settings: v for Settings, v in payload.model_dump().items() if v is not None}})
                updated = {pascal}Read(**data)
                self._items[item_id] = updated
                return updated

            def delete(self, item_id: int) -> bool:
                return self._items.pop(item_id, None) is not None
        ''')

    init_code = dedent(f'''\
        # Re-export commonly used pieces for convenience
        from .router import {router_var}  # noqa: F401
        from .schemas import {pascal}Create, {pascal}Read, {pascal}Update  # noqa: F401
        ''')


    write_file(router_py, router_code, args.force)
    write_file(schemas_py, schemas_code, args.force)
    write_file(service_py, service_code, args.force)
    write_file(repository_py, repository_code, args.force)
    write_file(init_py, init_code, args.force)

    print("\\nDone. To include the router in your FastAPI app:")
    print(f"  from {module_name}.router import {router_var}")
    print(f"  app.include_router({router_var})")

if __name__ == "__main__":
    main()
