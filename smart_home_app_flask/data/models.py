from pydantic import BaseModel, Field, ValidationError
from typing import Optional
from datetime import datetime

class TelemetryModel(BaseModel):
    temperature: float
    humidity: float
    light: float
    motion: float
    timestamp: datetime = Field(default_factory=datetime.now)

class MainLightSettings(BaseModel):
    defaultIntensity: int = Field(..., ge=0, le=100, description="Default brightness percentage")
    defaultPower: bool = Field(..., description="Default power state")

class CurtainsSettings(BaseModel):
    defaultPosition: int = Field(..., ge=0, le=100, description="Curtain open percentage")
    autoCloseTemp: float = Field(..., description="Temperature threshold to auto-close curtains")
    autoCloseTime: str = Field(..., pattern=r"^\d{2}:\d{2}$", description="Scheduled curtain close time")
    lightIntensityWhenClosed: int = Field(..., ge=0, le=100, description="Light intensity when curtains are closed")

class ClimateSettings(BaseModel):
    defaultMode: str = Field(..., pattern="^(cool|warm|off)$", description="Climate mode: cool, warm, or off")
    targetTemperature: float = Field(..., description="Target temperature for climate system")

class SecuritySystemSettings(BaseModel):
    defaultState: bool = Field(..., description="Default state of the security system")

class SettingsModel(BaseModel):
    mainLight: MainLightSettings
    curtains: CurtainsSettings
    climate: ClimateSettings
    securitySystem: SecuritySystemSettings
    createdAt: Optional[datetime] = Field(default_factory=datetime.now)
    updatedAt: Optional[datetime] = Field(default_factory=datetime.now)
