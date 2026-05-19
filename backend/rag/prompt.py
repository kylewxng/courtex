
def coords_to_zone(x, y) -> str:
    distance = (x**2 + y**2) ** 0.5

    if abs(x) <= 80 and y <= 140:
        return "paint"
    elif y < 90 and abs(x) > 220:
        return "corner"
    elif distance >= 238 and abs(x) > 150:
        return "wing"
    elif distance >= 238 and abs(x) <= 150:
        return "top of the key"
    elif distance < 238:
        return "mid-range"
    else:
        return "unknown"


def format_clock(clock: str) -> str:
    try:
        clock = clock.replace("PT", "").replace("S", "")
        minutes, seconds = clock.split("M")
        return f"{int(minutes)}:{int(float(seconds)):02d}"
    except Exception:
        return clock or "unknown"


def build_prompt(query: str, plays: list[dict]) -> str:
    lines = []
    for i, play in enumerate(plays, 1):
        zone = coords_to_zone(play.get("x_legacy", 0), play.get("y_legacy", 0))
        clock = format_clock(play.get("clock", ""))
        lines.append(
            f"{i}. Description: {play.get('description')} | Outcome: {play.get('action_type')} | Zone: {zone} | Time: {clock}"
        )

    plays_text = "\n".join(lines)
    return (
        f"You are an NBA play analyst. Answer the user's question using only the plays provided.\n\n"
        f"Format your response using markdown:\n"
        f"- Start with the heading: ## Top {len(plays)} Most Matched Plays\n"
        f"- List each play as a numbered item. Bold the player/shot description. Italicize the zone and time (e.g. *top of the key, at 8:03 remaining*). Put the outcome (Made/Missed) on the same line in bold.\n"
        f"- Leave a blank line between each play for readability\n"
        f"- End with a ## Analysis section: 2-3 sentences summarizing patterns or insights\n"
        f"- Do not mention game IDs or raw field names. Write naturally.\n\n"
        f"Question: {query}\n\n"
        f"Relevant plays:\n{plays_text}\n\n"
        f"Answer:"
    )


if __name__ == "__main__":
    sample_plays = [
        {"description": "Curry 3PT Jump Shot (8 PTS)", "action_type": "Made Shot", 
         "clock": "PT11M12.00S", "game_id": 22400132, "x_legacy": 223, "y_legacy": 2},
        {"description": "Curry 2' Driving Layup (7 PTS)", "action_type": "Made Shot", 
         "clock": "PT03M55.00S", "game_id": 22400188, "x_legacy": 10, "y_legacy": 12},
    ]
    print(build_prompt("Where does Curry shoot from?", sample_plays))

