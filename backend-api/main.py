from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, database, schema
# from database import engine, Base # Import engine and Base for creating the db.
from typing import List

# Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Tournament API Endpoints
@app.post("/tournaments/", response_model=schema.Tournament)
def create_tournament(tournament: schema.TournamentCreate, db: Session = Depends(get_db)):
    return crud.create_tournament(db=db, tournament=tournament)

@app.get("/tournaments/{tournament_id}", response_model=schema.Tournament)
def read_tournament(tournament_id: int, db: Session = Depends(get_db)):
    db_tournament = crud.get_tournament(db=db, tournament_id=tournament_id)
    if db_tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return db_tournament

@app.get("/tournaments/", response_model=List[schema.Tournament])
def read_tournaments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tournaments = crud.get_tournaments(db=db, skip=skip, limit=limit)
    return tournaments

@app.put("/tournaments/{tournament_id}", response_model=schema.Tournament)
def update_tournament(tournament_id: int, tournament: schema.TournamentUpdate, db: Session = Depends(get_db)):
    return crud.update_tournament(db=db, tournament_id=tournament_id, tournament=tournament)

@app.delete("/tournaments/{tournament_id}")
def delete_tournament(tournament_id: int, db: Session = Depends(get_db)):
    return crud.delete_tournament(db=db, tournament_id=tournament_id)


# Team API Endpoints
@app.post("/teams/", response_model=schema.Team)
def create_team(team: schema.TeamCreate, db: Session = Depends(get_db)):
    return crud.create_team(db=db, team=team)

@app.get("/teams/{team_id}", response_model=schema.Team)
def read_team(team_id: int, db: Session = Depends(get_db)):
    db_team = crud.get_team(db=db, team_id=team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team

@app.get("/teams/", response_model=List[schema.Team])
def read_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    teams = crud.get_teams(db=db, skip=skip, limit=limit)
    return teams

@app.put("/teams/{team_id}", response_model=schema.Team)
def update_team(team_id: int, team: schema.TeamUpdate, db: Session = Depends(get_db)):
    return crud.update_team(db=db, team_id=team_id, team=team)

@app.delete("/teams/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_db)):
    return crud.delete_team(db=db, team_id=team_id)

# User API Endpoints
@app.post("/users/", response_model=schema.User)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    # TODO: Implement password hashing properly (bcrypt) before storing!
    # For demonstration, replace with a placeholder hashing function.
    hashed_password = hash_password(user.password) # CALL A FUNCTION YOU DEFINE TO HASH THE PASSWORD
    user_dict = user.dict(exclude={"password"}) # exclude plain password for security
    return crud.create_user(db=db, user=schema.UserCreate(**user_dict))

@app.get("/users/{user_id}", response_model=schema.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/", response_model=List[schema.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users

@app.put("/users/{user_id}", response_model=schema.User)
def update_user(user_id: int, user: schema.UserUpdate, db: Session = Depends(get_db)):
    return crud.update_user(db=db, user_id=user_id, user=user)

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db=db, user_id=user_id)

# Player API Endpoints
@app.post("/players/", response_model=schema.Player)
def create_player(player: schema.PlayerCreate, db: Session = Depends(get_db)):
    return crud.create_player(db=db, player=player)

@app.get("/players/{player_id}", response_model=schema.Player)
def read_player(player_id: int, db: Session = Depends(get_db)):
    db_player = crud.get_player(db=db, player_id=player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player

@app.get("/players/", response_model=List[schema.Player])
def read_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    players = crud.get_players(db=db, skip=skip, limit=limit)
    return players

@app.put("/players/{player_id}", response_model=schema.Player)
def update_player(player_id: int, player: schema.PlayerUpdate, db: Session = Depends(get_db)):
    return crud.update_player(db=db, player_id=player_id, player=player)

@app.delete("/players/{player_id}")
def delete_player(player_id: int, db: Session = Depends(get_db)):
    return crud.delete_player(db=db, player_id=player_id)

# FantasyTeam API Endpoints
@app.post("/fantasyteams/", response_model=schema.FantasyTeam)
def create_fantasy_team(fantasy_team: schema.FantasyTeamCreate, db: Session = Depends(get_db)):
    return crud.create_fantasy_team(db=db, fantasy_team=fantasy_team)

@app.get("/fantasyteams/{fantasy_team_id}", response_model=schema.FantasyTeam)
def read_fantasy_team(fantasy_team_id: int, db: Session = Depends(get_db)):
    db_fantasy_team = crud.get_fantasy_team(db=db, fantasy_team_id=fantasy_team_id)
    if db_fantasy_team is None:
        raise HTTPException(status_code=404, detail="FantasyTeam not found")
    return db_fantasy_team

@app.get("/fantasyteams/", response_model=List[schema.FantasyTeam])
def read_fantasy_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    fantasy_teams = crud.get_fantasy_teams(db=db, skip=skip, limit=limit)
    return fantasy_teams

@app.put("/fantasyteams/{fantasy_team_id}", response_model=schema.FantasyTeam)
def update_fantasy_team(fantasy_team_id: int, fantasy_team: schema.FantasyTeamUpdate, db: Session = Depends(get_db)):
    return crud.update_fantasy_team(db=db, fantasy_team_id=fantasy_team_id, fantasy_team=fantasy_team)

@app.delete("/fantasyteams/{fantasy_team_id}")
def delete_fantasy_team(fantasy_team_id: int, db: Session = Depends(get_db)):
    return crud.delete_fantasy_team(db=db, fantasy_team_id=fantasy_team_id)

# FantasyTeamPlayer API Endpoints
@app.post("/fantasyteamplayers/", response_model=schema.FantasyTeamPlayer)
def create_fantasy_team_player(fantasy_team_player: schema.FantasyTeamPlayerCreate, db: Session = Depends(get_db)):
    return crud.create_fantasy_team_player(db=db, fantasy_team_player=fantasy_team_player)

@app.get("/fantasyteamplayers/{fantasy_team_player_id}", response_model=schema.FantasyTeamPlayer)
def read_fantasy_team_player(fantasy_team_player_id: int, db: Session = Depends(get_db)):
    db_fantasy_team_player = crud.get_fantasy_team_player(db=db, fantasy_team_player_id=fantasy_team_player_id)
    if db_fantasy_team_player is None:
        raise HTTPException(status_code=404, detail="FantasyTeamPlayer not found")
    return db_fantasy_team_player

@app.get("/fantasyteamplayers/", response_model=List[schema.FantasyTeamPlayer])
def read_fantasy_team_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    fantasy_team_players = crud.get_fantasy_team_players(db=db, skip=skip, limit=limit)
    return fantasy_team_players

@app.put("/fantasyteamplayers/{fantasy_team_player_id}", response_model=schema.FantasyTeamPlayer)
def update_fantasy_team_player(fantasy_team_player_id: int, fantasy_team_player: schema.FantasyTeamPlayerUpdate, db: Session = Depends(get_db)):
    return crud.update_fantasy_team_player(db=db, fantasy_team_player_id=fantasy_team_player_id, fantasy_team_player=fantasy_team_player)

@app.delete("/fantasyteamplayers/{fantasy_team_player_id}")
def delete_fantasy_team_player(fantasy_team_player_id: int, db: Session = Depends(get_db)):
    return crud.delete_fantasy_team_player(db=db, fantasy_team_player_id=fantasy_team_player_id)

# Gameweek API Endpoints
@app.post("/gameweeks/", response_model=schema.Gameweek)
def create_gameweek(gameweek: schema.GameweekCreate, db: Session = Depends(get_db)):
    return crud.create_gameweek(db=db, gameweek=gameweek)

@app.get("/gameweeks/{gameweek_id}", response_model=schema.Gameweek)
def read_gameweek(gameweek_id: int, db: Session = Depends(get_db)):
    db_gameweek = crud.get_gameweek(db=db, gameweek_id=gameweek_id)
    if db_gameweek is None:
        raise HTTPException(status_code=404, detail="Gameweek not found")
    return db_gameweek

@app.get("/gameweeks/", response_model=List[schema.Gameweek])
def read_gameweeks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    gameweeks = crud.get_gameweeks(db=db, skip=skip, limit=limit)
    return gameweeks

@app.put("/gameweeks/{gameweek_id}", response_model=schema.Gameweek)
def update_gameweek(gameweek_id: int, gameweek: schema.GameweekUpdate, db: Session = Depends(get_db)):
    return crud.update_gameweek(db=db, gameweek_id=gameweek_id, gameweek=gameweek)

@app.delete("/gameweeks/{gameweek_id}")
def delete_gameweek(gameweek_id: int, db: Session = Depends(get_db)):
    return crud.delete_gameweek(db=db, gameweek_id=gameweek_id)

# Match API Endpoints
@app.post("/matches/", response_model=schema.Match)
def create_match(match: schema.MatchCreate, db: Session = Depends(get_db)):
    return crud.create_match(db=db, match=match)

@app.get("/matches/{match_id}", response_model=schema.Match)
def read_match(match_id: int, db: Session = Depends(get_db)):
    db_match = crud.get_match(db=db, match_id=match_id)
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return db_match

@app.get("/matches/", response_model=List[schema.Match])
def read_matches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    matches = crud.get_matches(db=db, skip=skip, limit=limit)
    return matches

@app.put("/matches/{match_id}", response_model=schema.Match)
def update_match(match_id: int, match: schema.MatchUpdate, db: Session = Depends(get_db)):
    return crud.update_match(db=db, match_id=match_id, match=match)

@app.delete("/matches/{match_id}")
def delete_match(match_id: int, db: Session = Depends(get_db)):
    return crud.delete_match(db=db, match_id=match_id)

# PlayerMatchPerformance API Endpoints
@app.post("/playermatchperformances/", response_model=schema.PlayerMatchPerformance)
def create_player_match_performance(player_match_performance: schema.PlayerMatchPerformanceCreate, db: Session = Depends(get_db)):
    return crud.create_player_match_performance(db=db, player_match_performance=player_match_performance)

@app.get("/playermatchperformances/{player_match_performance_id}", response_model=schema.PlayerMatchPerformance)
def read_player_match_performance(player_match_performance_id: int, db: Session = Depends(get_db)):
    db_player_match_performance = crud.get_player_match_performance(db=db, player_match_performance_id=player_match_performance_id)
    if db_player_match_performance is None:
        raise HTTPException(status_code=404, detail="PlayerMatchPerformance not found")
    return db_player_match_performance

@app.get("/playermatchperformances/", response_model=List[schema.PlayerMatchPerformance])
def read_player_match_performances(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    player_match_performances = crud.get_player_match_performances(db=db, skip=skip, limit=limit)
    return player_match_performances

@app.put("/playermatchperformances/{player_match_performance_id}", response_model=schema.PlayerMatchPerformance)
def update_player_match_performance(player_match_performance_id: int, player_match_performance: schema.PlayerMatchPerformanceUpdate, db: Session = Depends(get_db)):
    return crud.update_player_match_performance(db=db, player_match_performance_id=player_match_performance_id, player_match_performance=player_match_performance)

@app.delete("/playermatchperformances/{player_match_performance_id}")
def delete_player_match_performance(player_match_performance_id: int, db: Session = Depends(get_db)):
    return crud.delete_player_match_performance(db=db, player_match_performance_id=player_match_performance_id)

# FantasyTeamGameweekScore API Endpoints
@app.post("/fantasyteamgameweekscores/", response_model=schema.FantasyTeamGameweekScore)
def create_fantasy_team_gameweek_score(fantasy_team_gameweek_score: schema.FantasyTeamGameweekScoreCreate, db: Session = Depends(get_db)):
    return crud.create_fantasy_team_gameweek_score(db=db, fantasy_team_gameweek_score=fantasy_team_gameweek_score)

@app.get("/fantasyteamgameweekscores/{fantasy_team_gameweek_score_id}", response_model=schema.FantasyTeamGameweekScore)
def read_fantasy_team_gameweek_score(fantasy_team_gameweek_score_id: int, db: Session = Depends(get_db)):
    db_fantasy_team_gameweek_score = crud.get_fantasy_team_gameweek_score(db=db, fantasy_team_gameweek_score_id=fantasy_team_gameweek_score_id)
    if db_fantasy_team_gameweek_score is None:
        raise HTTPException(status_code=404, detail="FantasyTeamGameweekScore not found")
    return db_fantasy_team_gameweek_score

@app.get("/fantasyteamgameweekscores/", response_model=List[schema.FantasyTeamGameweekScore])
def read_fantasy_team_gameweek_scores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    fantasy_team_gameweek_scores = crud.get_fantasy_team_gameweek_scores(db=db, skip=skip, limit=limit)
    return fantasy_team_gameweek_scores

@app.put("/fantasyteamgameweekscores/{fantasy_team_gameweek_score_id}", response_model=schema.FantasyTeamGameweekScore)
def update_fantasy_team_gameweek_score(fantasy_team_gameweek_score_id: int, fantasy_team_gameweek_score: schema.FantasyTeamGameweekScoreUpdate, db: Session = Depends(get_db)):
    return crud.update_fantasy_team_gameweek_score(db=db, fantasy_team_gameweek_score_id=fantasy_team_gameweek_score_id, fantasy_team_gameweek_score=fantasy_team_gameweek_score)

@app.delete("/fantasyteamgameweekscores/{fantasy_team_gameweek_score_id}")
def delete_fantasy_team_gameweek_score(fantasy_team_gameweek_score_id: int, db: Session = Depends(get_db)):
    return crud.delete_fantasy_team_gameweek_score(db=db, fantasy_team_gameweek_score_id=fantasy_team_gameweek_score_id)

# Example Password Hashing Function (REPLACE WITH BCRYPT)
def hash_password(password: str):
    # DO NOT USE THIS IN PRODUCTION.  IT'S JUST A PLACEHOLDER.
    # Use bcrypt, argon2, or a similar secure hashing algorithm.
    return "insecure_hash_" + password  #  Very insecure!