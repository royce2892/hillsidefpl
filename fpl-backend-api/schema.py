# schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# Tournament Schemas
class TournamentBase(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    description: Optional[str] = None


class TournamentCreate(TournamentBase):
    pass


class TournamentUpdate(TournamentBase):
    name: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    description: Optional[str] = None


class Tournament(TournamentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # Important: Allows Pydantic to work with SQLAlchemy models


# Team Schemas
class TeamBase(BaseModel):
    name: str
    tournament_id: int
    abbreviation: Optional[str] = None
    logo_url: Optional[str] = None


class TeamCreate(TeamBase):
    pass


class TeamUpdate(TeamBase):
    name: Optional[str] = None
    tournament_id: Optional[int] = None
    abbreviation: Optional[str] = None
    logo_url: Optional[str] = None


class Team(TeamBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# User Schemas
class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    mobile_number: Optional[str] = None
    flat_number: Optional[str] = None


class UserCreate(UserBase):
    password: str  # Request password during creation
    # hashed_password: str


class UserUpdate(UserBase):
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    mobile_number: Optional[str] = None
    flat_number: Optional[str] = None


class User(UserBase):
    id: int
    disabled: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# FantasyTeam Schemas
class FantasyTeamBase(BaseModel):
    name: str
    user_id: int
    tournament_id: int


class FantasyTeamCreate(FantasyTeamBase):
    pass


class FantasyTeamUpdate(FantasyTeamBase):
    name: Optional[str] = None
    user_id: Optional[int] = None
    tournament_id: Optional[int] = None


class FantasyTeam(FantasyTeamBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Player Schemas
class PlayerBase(BaseModel):
    team_id: int
    name: str
    position: str
    value: float


class PlayerCreate(PlayerBase):
    pass


class PlayerUpdate(PlayerBase):
    team_id: Optional[int] = None
    name: Optional[str] = None
    position: Optional[str] = None
    value: Optional[float] = None


class Player(PlayerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# FantasyTeamPlayer Schemas
class FantasyTeamPlayerBase(BaseModel):
    fantasy_team_id: int
    player_id: int
    is_captain: Optional[bool] = None


class FantasyTeamPlayerCreate(FantasyTeamPlayerBase):
    pass


class FantasyTeamPlayerUpdate(FantasyTeamPlayerBase):
    fantasy_team_id: Optional[int] = None
    player_id: Optional[int] = None
    is_captain: Optional[bool] = None


class FantasyTeamPlayer(FantasyTeamPlayerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Gameweek Schemas
class GameweekBase(BaseModel):
    tournament_id: int
    name: str
    start_date: datetime
    end_date: datetime


class GameweekCreate(GameweekBase):
    pass


class GameweekUpdate(GameweekBase):
    tournament_id: Optional[int] = None
    name: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[str] = None


class Gameweek(GameweekBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Match Schemas
class MatchBase(BaseModel):
    gameweek_id: int
    home_team_id: int
    away_team_id: int
    start_time: datetime
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    is_finished: Optional[bool] = None


class MatchCreate(MatchBase):
    pass


class MatchUpdate(MatchBase):
    gameweek_id: Optional[int] = None
    home_team_id: Optional[int] = None
    away_team_id: Optional[int] = None
    start_time: Optional[datetime] = None
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    is_finished: Optional[bool] = None


class Match(MatchBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# PlayerMatchPerformance Schemas
class PlayerMatchPerformanceBase(BaseModel):
    match_id: int
    player_id: int
    goals: int = 0
    assists: int = 0
    yellow_cards: int = 0
    red_cards: int = 0
    minutes_played: int = 0
    clean_sheet: bool = False
    own_goals: int = 0


class PlayerMatchPerformanceCreate(PlayerMatchPerformanceBase):
    pass


class PlayerMatchPerformanceUpdate(PlayerMatchPerformanceBase):
    match_id: Optional[int] = None
    player_id: Optional[int] = None
    goals: Optional[int] = None
    assists: Optional[int] = None
    yellow_cards: Optional[int] = None
    red_cards: Optional[int] = None
    minutes_played: Optional[int] = None
    clean_sheet: Optional[bool] = None
    own_goals: Optional[int] = None


class PlayerMatchPerformance(PlayerMatchPerformanceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class FantasyTeamGameweekScoreBase(BaseModel):
    fantasy_team_id: int
    gameweek_id: int
    total_points: float = 0.0


class FantasyTeamGameweekScoreCreate(FantasyTeamGameweekScoreBase):
    pass


class FantasyTeamGameweekScoreUpdate(FantasyTeamGameweekScoreBase):
    fantasy_team_id: Optional[int] = None
    gameweek_id: Optional[int] = None
    total_points: Optional[float] = None


class FantasyTeamGameweekScore(FantasyTeamGameweekScoreBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
