import hashlib
import hmac
import os
import uuid
from datetime import datetime, timezone

from fastapi import FastAPI, Request, Response, UploadFile, Form, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from dateutil import parser as dateparser

from . import data, db

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "turkey")
SESSION_SECRET = os.environ.get("SESSION_SECRET", "dev-secret-change-me")
OLYMPICS_UNLOCK_AT = os.environ.get("OLYMPICS_UNLOCK_AT", "2026-11-25T10:00:00-05:00")
SCAVENGER_UNLOCK_AT = os.environ.get("SCAVENGER_UNLOCK_AT", "2026-11-25T15:00:00-05:00")

OLYMPICS_UNLOCK_DT = dateparser.isoparse(OLYMPICS_UNLOCK_AT)
SCAVENGER_UNLOCK_DT = dateparser.isoparse(SCAVENGER_UNLOCK_AT)

ADMIN_TOKEN = hmac.new(SESSION_SECRET.encode(), ADMIN_PASSWORD.encode(), hashlib.sha256).hexdigest()

app = FastAPI()


@app.on_event("startup")
def startup():
    db.init()


def require_admin(request: Request):
    token = request.cookies.get("admin_token")
    if not token or not hmac.compare_digest(token, ADMIN_TOKEN):
        raise HTTPException(status_code=401, detail="Not logged in")


def all_task_lookup():
    """task_id -> task dict, across stops, battle cry, wildcards"""
    lookup = {data.BATTLE_CRY_TASK["id"]: data.BATTLE_CRY_TASK}
    for stop in data.STOPS.values():
        for t in stop["tasks"]:
            lookup[t["id"]] = t
    for t in data.WILDCARDS:
        lookup[t["id"]] = t
    return lookup


TASK_LOOKUP = all_task_lookup()


@app.get("/api/state")
def get_state():
    now = datetime.now(timezone.utc)
    olympics_unlocked = now >= OLYMPICS_UNLOCK_DT
    scavenger_unlocked = now >= SCAVENGER_UNLOCK_DT

    with db.get_conn() as conn:
        olympic_rows = conn.execute("SELECT * FROM olympic_scores").fetchall()
        sub_rows = conn.execute(
            "SELECT * FROM scavenger_submissions WHERE voided = 0"
        ).fetchall()
        bonus_rows = conn.execute("SELECT * FROM scavenger_bonuses").fetchall()
        showdown_rows = conn.execute("SELECT * FROM showdown_results").fetchall()

    olympic_scores = {}
    for row in olympic_rows:
        olympic_scores.setdefault(row["event_id"], {})[row["team"]] = row["points"]

    submissions = []
    completed_by_team = {"team1": set(), "team2": set()}
    scavenger_points = {"team1": 0, "team2": 0}
    for row in sub_rows:
        submissions.append(
            {
                "id": row["id"],
                "task_id": row["task_id"],
                "team": row["team"],
                "points": row["points"],
                "text_answer": row["text_answer"],
                "proof_path": row["proof_path"],
                "created_at": row["created_at"],
            }
        )
        completed_by_team.setdefault(row["team"], set()).add(row["task_id"])
        scavenger_points[row["team"]] = scavenger_points.get(row["team"], 0) + row["points"]

    bonuses = []
    for row in bonus_rows:
        bonuses.append({"id": row["id"], "team": row["team"], "label": row["label"], "points": row["points"]})
        scavenger_points[row["team"]] = scavenger_points.get(row["team"], 0) + row["points"]

    showdown_results = {row["showdown_id"]: row["winner_team"] for row in showdown_rows}
    for showdown in data.SHOWDOWNS:
        winner = showdown_results.get(showdown["id"])
        if winner:
            scavenger_points[winner] = scavenger_points.get(winner, 0) + 5

    olympics_total = {"team1": 0, "team2": 0}
    for event_id, by_team in olympic_scores.items():
        for team, pts in by_team.items():
            olympics_total[team] = olympics_total.get(team, 0) + pts

    combined_total = {
        team: olympics_total.get(team, 0) + scavenger_points.get(team, 0)
        for team in ("team1", "team2")
    }

    return {
        "now": now.isoformat(),
        "olympics_unlock_at": OLYMPICS_UNLOCK_DT.isoformat(),
        "scavenger_unlock_at": SCAVENGER_UNLOCK_DT.isoformat(),
        "olympics_unlocked": olympics_unlocked,
        "scavenger_unlocked": scavenger_unlocked,
        "teams": {"team1": data.TEAM_1, "team2": data.TEAM_2},
        "schedule": data.SCHEDULE,
        "olympic_events": data.OLYMPIC_EVENTS,
        "olympic_scores": olympic_scores,
        "olympics_total": olympics_total,
        "scavenger_submissions": submissions,
        "completed_task_ids": {k: sorted(v) for k, v in completed_by_team.items()},
        "scavenger_bonuses": bonuses,
        "scavenger_points": scavenger_points,
        "showdowns": data.SHOWDOWNS,
        "showdown_results": showdown_results,
        "combined_total": combined_total,
        "rules": data.SCAVENGER_RULES,
        "stops": data.STOPS,
        "battle_cry_task": data.BATTLE_CRY_TASK,
        "wildcards": data.WILDCARDS,
        "team_routes": data.TEAM_ROUTES,
    }


@app.post("/api/admin/login")
def admin_login(response: Response, password: str = Form(...)):
    if not hmac.compare_digest(password, ADMIN_PASSWORD):
        raise HTTPException(status_code=401, detail="Wrong password")
    response.set_cookie("admin_token", ADMIN_TOKEN, httponly=True, samesite="lax", max_age=60 * 60 * 24 * 7)
    return {"ok": True}


@app.post("/api/admin/logout")
def admin_logout(response: Response):
    response.delete_cookie("admin_token")
    return {"ok": True}


@app.get("/api/admin/check")
def admin_check(request: Request):
    token = request.cookies.get("admin_token")
    return {"logged_in": bool(token and hmac.compare_digest(token, ADMIN_TOKEN))}


@app.get("/api/admin/answer-key")
def admin_answer_key(request: Request):
    require_admin(request)
    return data.ANSWER_KEY


@app.post("/api/admin/olympics-score")
def set_olympics_score(request: Request, event_id: str = Form(...), team: str = Form(...), points: int = Form(...)):
    require_admin(request)
    if team not in ("team1", "team2"):
        raise HTTPException(400, "bad team")
    with db.get_conn() as conn:
        conn.execute(
            "INSERT INTO olympic_scores (event_id, team, points) VALUES (?, ?, ?) "
            "ON CONFLICT(event_id, team) DO UPDATE SET points = excluded.points",
            (event_id, team, points),
        )
        conn.commit()
    return {"ok": True}


@app.post("/api/admin/scavenger/bonus")
def add_bonus(request: Request, team: str = Form(...), label: str = Form(...), points: int = Form(...)):
    require_admin(request)
    if team not in ("team1", "team2"):
        raise HTTPException(400, "bad team")
    with db.get_conn() as conn:
        conn.execute(
            "INSERT INTO scavenger_bonuses (team, label, points) VALUES (?, ?, ?)",
            (team, label, points),
        )
        conn.commit()
    return {"ok": True}


@app.post("/api/admin/scavenger/void")
def void_submission(request: Request, submission_id: int = Form(...)):
    require_admin(request)
    with db.get_conn() as conn:
        conn.execute("UPDATE scavenger_submissions SET voided = 1 WHERE id = ?", (submission_id,))
        conn.commit()
    return {"ok": True}


@app.post("/api/admin/showdown")
def set_showdown_winner(request: Request, showdown_id: str = Form(...), winner_team: str = Form(...)):
    require_admin(request)
    if winner_team not in ("team1", "team2"):
        raise HTTPException(400, "bad team")
    with db.get_conn() as conn:
        conn.execute(
            "INSERT INTO showdown_results (showdown_id, winner_team) VALUES (?, ?) "
            "ON CONFLICT(showdown_id) DO UPDATE SET winner_team = excluded.winner_team",
            (showdown_id, winner_team),
        )
        conn.commit()
    return {"ok": True}


@app.post("/api/scavenger/submit")
async def submit_task(
    task_id: str = Form(...),
    team: str = Form(...),
    text_answer: str = Form(None),
    proof: UploadFile = File(None),
):
    if team not in ("team1", "team2"):
        raise HTTPException(400, "bad team")
    task = TASK_LOOKUP.get(task_id)
    if not task:
        raise HTTPException(404, "unknown task")

    proof_path = None
    if proof is not None and proof.filename:
        ext = os.path.splitext(proof.filename)[1][:10]
        fname = f"{uuid.uuid4().hex}{ext}"
        dest = os.path.join(db.UPLOADS_DIR, fname)
        content = await proof.read()
        with open(dest, "wb") as f:
            f.write(content)
        proof_path = f"/uploads/{fname}"

    with db.get_conn() as conn:
        conn.execute(
            "INSERT INTO scavenger_submissions (task_id, team, points, text_answer, proof_path) "
            "VALUES (?, ?, ?, ?, ?)",
            (task_id, team, task["points"], text_answer, proof_path),
        )
        conn.commit()
    return {"ok": True}


@app.get("/uploads/{filename}")
def get_upload(filename: str):
    path = os.path.join(db.UPLOADS_DIR, filename)
    if not os.path.isfile(path):
        raise HTTPException(404)
    return FileResponse(path)


app.mount("/", StaticFiles(directory="static", html=True), name="static")
