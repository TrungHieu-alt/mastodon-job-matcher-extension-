"""ChromaDB connection management."""

import chromadb
from chromadb.config import Settings as ChromaSettings
from loguru import logger
from typing import Optional

from config.settings import settings


class ChromaConnection:
    """Manages ChromaDB connection and initialization."""
    
    def __init__(self):
        """Initialize ChromaDB connection."""
        self._client: Optional[chromadb.PersistentClient] = None
        self._cv_collection = None
        self._jd_collection = None
        self._initialize_connection()
    
    def _initialize_connection(self):
        """Initialize ChromaDB client connection."""
        try:
            self._client = chromadb.PersistentClient(
                path=settings.chroma_persist_directory,
                settings=ChromaSettings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            logger.info(f"ChromaDB client initialized at {settings.chroma_persist_directory}")
            self._initialize_collections()
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB client: {e}")
            raise
    
    def _initialize_collections(self):
        """Initialize CV and job description collections."""
        try:
            # CV Collection
            try:
                self._cv_collection = self._client.get_collection("cvs")
                logger.info("Connected to existing CV collection")
            except ValueError:
                self._cv_collection = self._client.create_collection(
                    name="cvs",
                    metadata={"description": "CV documents and embeddings"}
                )
                logger.info("Created new CV collection")
            
            # Job Description Collection
            try:
                self._jd_collection = self._client.get_collection("job_descriptions")
                logger.info("Connected to existing job descriptions collection")
            except ValueError:
                self._jd_collection = self._client.create_collection(
                    name="job_descriptions",
                    metadata={"description": "Job description documents and embeddings"}
                )
                logger.info("Created new job descriptions collection")
                
        except Exception as e:
            logger.error(f"Failed to initialize collections: {e}")
            raise
    
    @property
    def client(self) -> chromadb.PersistentClient:
        """Get ChromaDB client."""
        if self._client is None:
            self._initialize_connection()
        return self._client
    
    @property
    def cv_collection(self):
        """Get CV collection."""
        return self._cv_collection
    
    @property
    def jd_collection(self):
        """Get job description collection."""
        return self._jd_collection
    
    def test_connection(self) -> bool:
        """Test ChromaDB connection."""
        try:
            collections = self._client.list_collections()
            logger.info(f"ChromaDB connection test successful. Collections: {len(collections)}")
            return True
        except Exception as e:
            logger.error(f"ChromaDB connection test failed: {e}")
            return False


# Global connection instance
chroma_connection = ChromaConnection()
