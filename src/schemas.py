from __future__ import annotations
from typing import List, Optional
from datetime import datetime
from src.service import S3Service
from src.orm import *




class User(FaunaModel):
    """User model."""
    sub: str = Field(...,index=True)
    nickname: Optional[str] = Field(default=None)
    name:Optional[str] = Field(default=None)
    picture: Optional[str] = Field(default=None)
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat(),index=True)
    email:Optional[str] = Field(default=None,index=True)
    email_verified:Optional[bool] = Field(default=None,index=True)
 
    def upsert(self):
        """Upsert a user."""
        user = User.q()(q.get(q.match(q.index("user_by_sub"), self.sub)))
        if user:
            user = User(**user["data"])
            return user.dict()
        else:
            return self.create()

    @classmethod
    def find_by_sub(cls, sub: str) -> User:
        """Get a user by its sub."""
        return cls.q()(q.get(q.match(q.index("user_by_sub"), sub)))["data"]

class CodePen(FaunaModel):
    """Data Model for CodePencils"""
    title: str = Field(..., index=True)
    description: Optional[str] = Field(default=None)
    tags: List[str] = Field(default_factory=list, unique_items=True, index=True)
    key: str = Field(..., index=True)
    sub: str = Field(..., index=True)
    url:str = Field(...)
    created_at: str = Field(
        default_factory=lambda: datetime.now().isoformat(), index=True
    )
    updated_at: str = Field(
        default_factory=lambda: datetime.now().isoformat(), index=True
    )
    
    @classmethod
    def service(cls):
        return S3Service()
    
    
    @classmethod
    def find_by_key(cls, key: str) -> CodePen:
        """Get a CodePen by its key."""
        codepen = cls.q()(q.get(q.match(q.index("codepen_by_key"), key)))["data"]
        obj = cls(**codepen)
        return obj
    
    @classmethod
    def find_by_sub(cls, sub: str) -> List[CodePen]:
        """Get all CodePens by a user's sub."""
        codepens = cls.q()(q.paginate(q.match(q.index("codepen_by_sub"), sub)))["data"]
        return [cls(**codepen) for codepen in codepens]
    
    
    @classmethod
    def find_many(cls) :
        """Get all CodePens."""
        refs = cls.q()(q.paginate(q.match(q.index("codepen_all"))))["data"]
        for ref in refs:
            obj = cls.q()(q.get(ref))["data"]
            obj["user"] = User.find_by_sub(obj["sub"])
            yield obj
    
    
    def upsert(self):
        """Upsert a user."""
        codepen = CodePen.q()(q.get(q.match(q.index("codepen_by_key"), self.key)))
        if codepen:
            codepen = User(**codepen["data"])
            return codepen.dict()
        else:
            return self.create()

    @classmethod
    def delete_by_key(cls, key: str):
        """Delete a CodePen by its key."""
        ref = cls.q()(q.get(q.match(q.index("codepen_by_key"), key)))
        cls.q()(q.delete(ref["ref"]))
        S3Service().delete_file(key)
