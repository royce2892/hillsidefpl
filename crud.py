# crud.py
from sqlalchemy.orm import Session
import database
import schema
from fastapi import HTTPException
from typing import List

# Tournament CRUD

def get_tournament(db: Session, tournament_id: int):
    return db.query(database.Tournament).filter(database.Tournament.id == tournament_id).first()

def get_tournaments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.Tournament).offset(skip).limit(limit).all()

def create_tournament(db: Session, tournament: schema.TournamentCreate):
    db_tournament = database.Tournament(**tournament.dict())
    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament

def update_tournament(db: Session, tournament_id: int, tournament: schema.TournamentUpdate):
    db_tournament = get_tournament(db, tournament_id=tournament_id)
    if db_tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found")

    for key, value in tournament.dict(exclude_unset=True).items():
        setattr(db_tournament, key, value)

    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament

def delete_tournament(db: Session, tournament_id: int):
    db_tournament = get_tournament(db, tournament_id=tournament_id)
    if db_tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found")

    db.delete(db_tournament)
    db.commit()
    return {"message": "Tournament deleted successfully"}


# Team CRUD

def get_team(db: Session, team_id: int):
    return db.query(database.Team).filter(database.Team.id == team_id).first()

def get_teams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.Team).offset(skip).limit(limit).all()

def create_team(db: Session, team: schema.TeamCreate):
    db_team = database.Team(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def update_team(db: Session, team_id: int, team: schema.TeamUpdate):
    db_team = get_team(db, team_id=team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    for key, value in team.dict(exclude_unset=True).items():
        setattr(db_team, key, value)

    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def delete_team(db: Session, team_id: int):
    db_team = get_team(db, team_id=team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    db.delete(db_team)
    db.commit()
    return {"message": "Team deleted successfully"}

# User CRUD
def get_user(db: Session, user_id: int):
    return db.query(database.User).filter(database.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(database.User).filter(database.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schema.UserCreate):
    # Hash the password before storing it
    # hashed_password = # TODO: Replace with bcrypt or similar hashing
    hashed_password = user.password
    db_user = database.User(**user.dict(exclude={"password"}), hashed_password=hashed_password)  # Exclude plain password
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: schema.UserUpdate):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

# Player CRUD

def get_player(db: Session, player_id: int):
    return db.query(database.Player).filter(database.Player.id == player_id).first()


def get_players(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.Player).offset(skip).limit(limit).all()


def create_player(db: Session, player: schema.PlayerCreate):
    db_player = database.Player(**player.dict())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


def update_player(db: Session, player_id: int, player: schema.PlayerUpdate):
    db_player = get_player(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")

    for key, value in player.dict(exclude_unset=True).items():
        setattr(db_player, key, value)

    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


def delete_player(db: Session, player_id: int):
    db_player = get_player(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")

    db.delete(db_player)
    db.commit()
    return {"message": "Player deleted successfully"}


# FantasyTeam CRUD

def get_fantasy_team(db: Session, fantasy_team_id: int):
    return db.query(database.FantasyTeam).filter(database.FantasyTeam.id == fantasy_team_id).first()


def get_fantasy_teams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.FantasyTeam).offset(skip).limit(limit).all()


def create_fantasy_team(db: Session, fantasy_team: schema.FantasyTeamCreate):
    db_fantasy_team = database.FantasyTeam(**fantasy_team.dict())
    db.add(db_fantasy_team)
    db.commit()
    db.refresh(db_fantasy_team)
    return db_fantasy_team


def update_fantasy_team(db: Session, fantasy_team_id: int, fantasy_team: schema.FantasyTeamUpdate):
    db_fantasy_team = get_fantasy_team(db, fantasy_team_id=fantasy_team_id)
    if db_fantasy_team is None:
        raise HTTPException(status_code=404, detail="FantasyTeam not found")

    for key, value in fantasy_team.dict(exclude_unset=True).items():
        setattr(db_fantasy_team, key, value)

    db.add(db_fantasy_team)
    db.commit()
    db.refresh(db_fantasy_team)
    return db_fantasy_team


def delete_fantasy_team(db: Session, fantasy_team_id: int):
    db_fantasy_team = get_fantasy_team(db, fantasy_team_id=fantasy_team_id)
    if db_fantasy_team is None:
        raise HTTPException(status_code=404, detail="FantasyTeam not found")

    db.delete(db_fantasy_team)
    db.commit()
    return {"message": "FantasyTeam deleted successfully"}


# FantasyTeamPlayer CRUD

def get_fantasy_team_player(db: Session, fantasy_team_player_id: int):
    return db.query(database.FantasyTeamPlayer).filter(database.FantasyTeamPlayer.id == fantasy_team_player_id).first()


def get_fantasy_team_players(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.FantasyTeamPlayer).offset(skip).limit(limit).all()


def create_fantasy_team_player(db: Session, fantasy_team_player: schema.FantasyTeamPlayerCreate):
    db_fantasy_team_player = database.FantasyTeamPlayer(**fantasy_team_player.dict())
    db.add(db_fantasy_team_player)
    db.commit()
    db.refresh(db_fantasy_team_player)
    return db_fantasy_team_player


def update_fantasy_team_player(db: Session, fantasy_team_player_id: int, fantasy_team_player: schema.FantasyTeamPlayerUpdate):
    db_fantasy_team_player = get_fantasy_team_player(db, fantasy_team_player_id=fantasy_team_player_id)
    if db_fantasy_team_player is None:
        raise HTTPException(status_code=404, detail="FantasyTeamPlayer not found")

    for key, value in fantasy_team_player.dict(exclude_unset=True).items():
        setattr(db_fantasy_team_player, key, value)

    db.add(db_fantasy_team_player)
    db.commit()
    db.refresh(db_fantasy_team_player)
    return db_fantasy_team_player


def delete_fantasy_team_player(db: Session, fantasy_team_player_id: int):
    db_fantasy_team_player = get_fantasy_team_player(db, fantasy_team_player_id=fantasy_team_player_id)
    if db_fantasy_team_player is None:
        raise HTTPException(status_code=404, detail="FantasyTeamPlayer not found")

    db.delete(db_fantasy_team_player)
    db.commit()
    return {"message": "FantasyTeamPlayer deleted successfully"}

# Gameweek CRUD

def get_gameweek(db: Session, gameweek_id: int):
    return db.query(database.Gameweek).filter(database.Gameweek.id == gameweek_id).first()


def get_gameweeks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.Gameweek).offset(skip).limit(limit).all()


def create_gameweek(db: Session, gameweek: schema.GameweekCreate):
    db_gameweek = database.Gameweek(**gameweek.dict())
    db.add(db_gameweek)
    db.commit()
    db.refresh(db_gameweek)
    return db_gameweek


def update_gameweek(db: Session, gameweek_id: int, gameweek: schema.GameweekUpdate):
    db_gameweek = get_gameweek(db, gameweek_id=gameweek_id)
    if db_gameweek is None:
        raise HTTPException(status_code=404, detail="Gameweek not found")

    for key, value in gameweek.dict(exclude_unset=True).items():
        setattr(db_gameweek, key, value)

    db.add(db_gameweek)
    db.commit()
    db.refresh(db_gameweek)
    return db_gameweek


def delete_gameweek(db: Session, gameweek_id: int):
    db_gameweek = get_gameweek(db, gameweek_id=gameweek_id)
    if db_gameweek is None:
        raise HTTPException(status_code=404, detail="Gameweek not found")

    db.delete(db_gameweek)
    db.commit()
    return {"message": "Gameweek deleted successfully"}


# Match CRUD

def get_match(db: Session, match_id: int):
    return db.query(database.Match).filter(database.Match.id == match_id).first()


def get_matches(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.Match).offset(skip).limit(limit).all()


def create_match(db: Session, match: schema.MatchCreate):
    db_match = database.Match(**match.dict())
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match


def update_match(db: Session, match_id: int, match: schema.MatchUpdate):
    db_match = get_match(db, match_id=match_id)
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")

    for key, value in match.dict(exclude_unset=True).items():
        setattr(db_match, key, value)

    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match


def delete_match(db: Session, match_id: int):
    db_match = get_match(db, match_id=match_id)
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")

    db.delete(db_match)
    db.commit()
    return {"message": "Match deleted successfully"}

# PlayerMatchPerformance CRUD

def get_player_match_performance(db: Session, player_match_performance_id: int):
    return db.query(database.PlayerMatchPerformance).filter(database.PlayerMatchPerformance.id == player_match_performance_id).first()


def get_player_match_performances(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.PlayerMatchPerformance).offset(skip).limit(limit).all()


def create_player_match_performance(db: Session, player_match_performance: schema.PlayerMatchPerformanceCreate):
    db_player_match_performance = database.PlayerMatchPerformance(**player_match_performance.dict())
    db.add(db_player_match_performance)
    db.commit()
    db.refresh(db_player_match_performance)
    return db_player_match_performance


def update_player_match_performance(db: Session, player_match_performance_id: int, player_match_performance: schema.PlayerMatchPerformanceUpdate):
    db_player_match_performance = get_player_match_performance(db, player_match_performance_id=player_match_performance_id)
    if db_player_match_performance is None:
        raise HTTPException(status_code=404, detail="PlayerMatchPerformance not found")

    for key, value in player_match_performance.dict(exclude_unset=True).items():
        setattr(db_player_match_performance, key, value)

    db.add(db_player_match_performance)
    db.commit()
    db.refresh(db_player_match_performance)
    return db_player_match_performance


def delete_player_match_performance(db: Session, player_match_performance_id: int):
    db_player_match_performance = get_player_match_performance(db, player_match_performance_id=player_match_performance_id)
    if db_player_match_performance is None:
        raise HTTPException(status_code=404, detail="PlayerMatchPerformance not found")

    db.delete(db_player_match_performance)
    db.commit()
    return {"message": "PlayerMatchPerformance deleted successfully"}

# FantasyTeamGameweekScore CRUD

def get_fantasy_team_gameweek_score(db: Session, fantasy_team_gameweek_score_id: int):
    return db.query(database.FantasyTeamGameweekScore).filter(database.FantasyTeamGameweekScore.id == fantasy_team_gameweek_score_id).first()


def get_fantasy_team_gameweek_scores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.FantasyTeamGameweekScore).offset(skip).limit(limit).all()


def create_fantasy_team_gameweek_score(db: Session, fantasy_team_gameweek_score: schema.FantasyTeamGameweekScoreCreate):
    db_fantasy_team_gameweek_score = database.FantasyTeamGameweekScore(**fantasy_team_gameweek_score.dict())
    db.add(db_fantasy_team_gameweek_score)
    db.commit()
    db.refresh(db_fantasy_team_gameweek_score)
    return db_fantasy_team_gameweek_score


def update_fantasy_team_gameweek_score(db: Session, fantasy_team_gameweek_score_id: int, fantasy_team_gameweek_score: schema.FantasyTeamGameweekScoreUpdate):
    db_fantasy_team_gameweek_score = get_fantasy_team_gameweek_score(db, fantasy_team_gameweek_score_id=fantasy_team_gameweek_score_id)
    if db_fantasy_team_gameweek_score is None:
        raise HTTPException(status_code=404, detail="FantasyTeamGameweekScore not found")

    for key, value in fantasy_team_gameweek_score.dict(exclude_unset=True).items():
        setattr(db_fantasy_team_gameweek_score, key, value)

    db.add(db_fantasy_team_gameweek_score)
    db.commit()
    db.refresh(db_fantasy_team_gameweek_score)
    return db_fantasy_team_gameweek_score


def delete_fantasy_team_gameweek_score(db: Session, fantasy_team_gameweek_score_id: int):
    db_fantasy_team_gameweek_score = get_fantasy_team_gameweek_score(db, fantasy_team_gameweek_score_id=fantasy_team_gameweek_score_id)
    if db_fantasy_team_gameweek_score is None:
        raise HTTPException(status_code=404, detail="FantasyTeamGameweekScore not found")

    db.delete(db_fantasy_team_gameweek_score)
    db.commit()
    return {"message": "FantasyTeamGameweekScore deleted successfully"}