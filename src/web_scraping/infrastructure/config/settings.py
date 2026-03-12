"""Application settings for the web scraping project."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Store runtime configuration for the application."""

    api_title: str = "Web Scraping Agents API"
    api_version: str = "0.1.0"
    default_city: str = "palmeira"
    notification_recipient: str = "vitorfelipep@dmmv-tech.com"
    model_config = SettingsConfigDict(env_prefix="WEB_SCRAPING_", extra="ignore")
