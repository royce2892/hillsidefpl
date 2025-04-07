from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Boolean, JSON
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()

class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    teams = relationship("Team", back_populates="tournament")
    gameweeks = relationship("Gameweek", back_populates="tournament")

    def __repr__(self):
        return f"<Tournament(id={self.id}, name='{self.name}')>"


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"))  # Relationship to Tournament
    abbreviation = Column(String(3), nullable=True)  # e.g., "ARS"
    logo_url = Column(String, nullable=True) # url to the team logo
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


    tournament = relationship("Tournament", back_populates="teams")
    players = relationship("Player", back_populates="team")
    home_matches = relationship("Match", back_populates="home_team", foreign_keys="[Match.home_team_id]")
    away_matches = relationship("Match", back_populates="away_team", foreign_keys="[Match.away_team_id]")

    def __repr__(self):
        return f"<Team(id={self.id}, name='{self.name}')>"

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"))  # Relationship to Team
    name = Column(String)
    position = Column(String)  # e.g., 'Forward', 'Midfielder', 'Defender', 'Goalkeeper'
    value = Column(Float)  # Player's value in the fantasy league (e.g., 7.5 million)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    team = relationship("Team", back_populates="players")
    match_performances = relationship("PlayerMatchPerformance", back_populates="player")

    def __repr__(self):
        return f"<Player(id={self.id}, name='{self.name} )>"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String) # Store securely!  Use bcrypt or similar.
    full_name = Column(String, nullable=True)
    disabled = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    mobile_number = Column(String, nullable=True) # Added mobile number
    flat_number = Column(String, nullable=True) # Added flat number
    fantasy_teams = relationship("FantasyTeam", back_populates="owner")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

class FantasyTeam(Base):
    __tablename__ = "fantasy_teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))  # Owner of the team
    tournament_id = Column(Integer, ForeignKey("tournaments.id"))  # Tournament the team is participating in
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    owner = relationship("User", back_populates="fantasy_teams")
    tournament = relationship("Tournament")
    players = relationship("FantasyTeamPlayer", back_populates="fantasy_team")
    gameweek_scores = relationship("FantasyTeamGameweekScore", back_populates="fantasy_team")

    def __repr__(self):
        return f"<FantasyTeam(id={self.id}, name='{self.name}')>"

class FantasyTeamPlayer(Base):
    __tablename__ = "fantasy_team_players"

    id = Column(Integer, primary_key=True, index=True)
    fantasy_team_id = Column(Integer, ForeignKey("fantasy_teams.id"))
    player_id = Column(Integer, ForeignKey("players.id"))
    is_captain = Column(Boolean, default=False)  # Optional: Designate a captain for bonus points.
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


    fantasy_team = relationship("FantasyTeam", back_populates="players")
    player = relationship("Player")  #Direct relationship to the Player table

    def __repr__(self):
        return f"<FantasyTeamPlayer(fantasy_team_id={self.fantasy_team_id}, player_id={self.player_id})>"

class FantasyTeamGameweekScore(Base):
    __tablename__ = "fantasy_team_gameweek_scores"

    id = Column(Integer, primary_key=True, index=True)
    fantasy_team_id = Column(Integer, ForeignKey("fantasy_teams.id"))
    gameweek_id = Column(Integer, ForeignKey("gameweeks.id"))
    total_points = Column(Float, default=0.0) # Total points for the fantasy team in this gameweek.
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    player_points = Column(JSON, nullable=True)
    # Requires SQLAlchemy >= 1.4 and a compatible database (PostgreSQL)
    # This would store a dictionary like: {player_id: points, player_id2: points2, ...}
    # Alternatively, you could create a separate table FantasyTeamGameweekPlayerScore

    fantasy_team = relationship("FantasyTeam", back_populates="gameweek_scores")
    gameweek = relationship("Gameweek")

    def __repr__(self):
        return f"<FantasyTeamGameweekScore(fantasy_team_id={self.fantasy_team_id}, gameweek_id={self.gameweek_id}, total_points={self.total_points})>"


class Gameweek(Base):
    __tablename__ = "gameweeks"

    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"))
    name = Column(String)  # e.g., "Gameweek 1", "Round 2"
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    tournament = relationship("Tournament", back_populates="gameweeks")
    matches = relationship("Match", back_populates="gameweek")

    def __repr__(self):
        return f"<Gameweek(id={self.id}, name='{self.name}')>"


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    gameweek_id = Column(Integer, ForeignKey("gameweeks.id"))
    home_team_id = Column(Integer, ForeignKey("teams.id"))
    away_team_id = Column(Integer, ForeignKey("teams.id"))
    start_time = Column(DateTime)
    home_score = Column(Integer, nullable=True, default=None)
    away_score = Column(Integer, nullable=True, default=None)
    is_finished = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    gameweek = relationship("Gameweek", back_populates="matches")
    home_team = relationship("Team", back_populates="home_matches", foreign_keys=[home_team_id])
    away_team = relationship("Team", back_populates="away_matches", foreign_keys=[away_team_id])


    def __repr__(self):
        return f"<Match(id={self.id}, home_team_id={self.home_team_id}, away_team_id={self.away_team_id})>"

class PlayerMatchPerformance(Base):
    __tablename__ = "player_match_performances"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"))
    player_id = Column(Integer, ForeignKey("players.id"))
    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    yellow_cards = Column(Integer, default=0)
    red_cards = Column(Integer, default=0)
    minutes_played = Column(Integer, default=0) # Important for calculating points.  DNP = 0
    clean_sheet = Column(Boolean, default=False) # Important for defenders and goalkeepers
    own_goals = Column(Integer, default=0)
    # Add other relevant stats here (e.g., saves for goalkeepers, penalties saved/missed, etc.)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    player = relationship("Player", back_populates="match_performances")
    match = relationship("Match")


# Database setup (example)
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/hillsidefpl"
engine = create_engine(DATABASE_URL)
# Base.metadata.drop_all(engine)  # WARNING: This will delete all data!
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == '__main__':
    # Example Usage and Testing
    from sqlalchemy.orm import Session

    def create_initial_data(db: Session):
        """Creates initial data for the database."""

        tournament = Tournament(name="PHG Football Cup 2025", start_date=func.now(), end_date=func.now())
        db.add(tournament)
        db.commit()
        db.refresh(tournament)

        team_mobin = Team(name="Team Mobin", tournament_id=tournament.id)
        team_ashwin = Team(name="Hillside United", tournament_id=tournament.id)
        team_anoop = Team(name="Athletico Hillside", tournament_id=tournament.id)
        team_anzer = Team(name="Real Hillsid", tournament_id=tournament.id)

        teams = [team_mobin, team_ashwin, team_anoop, team_anzer]
        db.add_all(teams)
        db.commit()
        for team in teams:
            db.refresh(team)

        g1 = Player(team_id=team_mobin.id, name="Royce", position="Forward", value=0.0)
        g2 = Player(team_id=team_mobin.id, name="Ashwin S", position="Midfielder", value=0.0)
        g3 = Player(team_id=team_mobin.id, name="Anoop Mammachen", position="Defender", value=0.0)
        g4 = Player(team_id=team_mobin.id, name="Jerry", position="Goalkeeper", value=0.0)
        g5 = Player(team_id=team_mobin.id, name="Jijo", position="Midfielder", value=0.0)
        g6 = Player(team_id=team_mobin.id, name="Sanal", position="Defender", value=0.0)
        g7 = Player(team_id=team_mobin.id, name="Ajith K", position="Forward", value=0.0)
        g8 = Player(team_id=team_mobin.id, name="Renju", position="Defender", value=0.0)

        u1 = Player(team_id=team_anoop.id, name="Joe", position="Forward", value=0.0)
        u2 = Player(team_id=team_anoop.id, name="Nishant", position="Midfielder", value=0.0)
        u3 = Player(team_id=team_anoop.id, name="Anzer", position="Defender", value=0.0)
        u4 = Player(team_id=team_anoop.id, name="Arun", position="Goalkeeper", value=0.0)
        u5 = Player(team_id=team_anoop.id, name="Antony", position="Midfielder", value=0.0)
        u6 = Player(team_id=team_anoop.id, name="Rahul", position="Defender", value=0.0)
        u7 = Player(team_id=team_anoop.id, name="Shiv", position="Forward", value=0.0)
        u8 = Player(team_id=team_anoop.id, name="Vishal", position="Defender", value=0.0)

        r1 = Player(team_id=team_ashwin.id, name="Alex", position="Forward", value=0.0)
        r2 = Player(team_id=team_ashwin.id, name="Hari", position="Midfielder", value=0.0)
        r3 = Player(team_id=team_ashwin.id, name="Jithin", position="Defender", value=0.0)
        r4 = Player(team_id=team_ashwin.id, name="Amal", position="Goalkeeper", value=0.0)
        r5 = Player(team_id=team_ashwin.id, name="Benny", position="Midfielder", value=0.0)
        r6 = Player(team_id=team_ashwin.id, name="Diwin", position="Defender", value=0.0)
        r7 = Player(team_id=team_ashwin.id, name="Rajesh", position="Forward", value=0.0)
        r8 = Player(team_id=team_ashwin.id, name="Ricky", position="Defender", value=0.0)

        a1 = Player(team_id=team_anzer.id, name="Jishnu", position="Forward", value=0.0)
        a2 = Player(team_id=team_anzer.id, name="Ashwin J", position="Midfielder", value=0.0)
        a3 = Player(team_id=team_anzer.id, name="Sreejith", position="Defender", value=0.0)
        a4 = Player(team_id=team_anzer.id, name="Ajit", position="Goalkeeper", value=0.0)
        a5 = Player(team_id=team_anzer.id, name="Kiran", position="Midfielder", value=0.0)
        a6 = Player(team_id=team_anzer.id, name="Vishnu", position="Defender", value=0.0)
        a7 = Player(team_id=team_anzer.id, name="Nizar", position="Forward", value=0.0)
        a8 = Player(team_id=team_anzer.id, name="Mobin", position="Defender", value=0.0)

        players = [g1, g2, g3, g4, g5, g6, g7, g8, u1, u2, u3, u4, u5, u6, u7, u8,
                   r1, r2, r3, r4, r5, r6, r7, r8, a1, a2, a3, a4, a5, a6, a7, a8]
        db.add_all(players)
        db.commit()
        for player in players:
            db.refresh(player)

        user1 = User(username="royce2892", email="royce2892@gmail.com", hashed_password="hashed_password")
        db.add(user1)
        db.commit()
        db.refresh(user1)

        fantasy_team = FantasyTeam(name="AWengers", user_id=user1.id, tournament_id=tournament.id)
        db.add(fantasy_team)
        db.commit()
        db.refresh(fantasy_team)

        fantasy_team_player = FantasyTeamPlayer(fantasy_team_id=fantasy_team.id, player_id=g1.id)
        db.add(fantasy_team_player)
        db.commit()


        gameweek1 = Gameweek(tournament_id=tournament.id, name="Gameweek 1", start_date=func.now(), end_date=func.now())
        db.add(gameweek1)
        db.commit()
        db.refresh(gameweek1)

        match1 = Match(gameweek_id=gameweek1.id, home_team_id=team_mobin.id, away_team_id=team_ashwin.id, start_time=func.now())
        db.add(match1)
        db.commit()
        db.refresh(match1)

        player_match_performance = PlayerMatchPerformance(match_id=match1.id, player_id=g1.id, goals=1, assists=1, minutes_played=90)
        db.add(player_match_performance)
        db.commit()

        fantasy_team_gameweek_score = FantasyTeamGameweekScore(fantasy_team_id=fantasy_team.id, gameweek_id=gameweek1.id, total_points=15.0)
        db.add(fantasy_team_gameweek_score)
        db.commit()

        print("Initial data created.")


    # Create a session
    db: Session = SessionLocal()

    # Check if tournament data exists. If not, create it.
    if db.query(Tournament).count() == 0:
        create_initial_data(db)
    else:
        print("Tournament data already exists. Skipping initialization.")


    # Example query
    tournament = db.query(Tournament).first()
    print(f"Tournament: {tournament}")

    db.close()