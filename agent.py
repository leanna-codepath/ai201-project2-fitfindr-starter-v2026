"""
The FitFindr planning loop.

This is the file that makes FitFindr an agent rather than a script. It decides
which tool to run next based on what the last one returned.

If your loop calls all three tools no matter what comes back, you have a list
of function calls. A loop looks at the last result before it picks the next
step. **That branch is the graded part of this unit.**

Build and test your three tools in `tools.py` first. Then come here.

    python agent.py          runs both example paths below
"""

import config
import trace
from tools import search_listings, suggest_outfit, create_fit_card
from generate import ModelUnavailable


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """
    A fresh session for one user interaction.

    The session is the single source of truth for a run. Every tool result goes
    in here, and the next tool reads it back out.

    You could pass values straight from one call to the next. It would work,
    and you would not be able to test it — you can't print a variable you have
    already overwritten. Going through the session is what makes the state
    visible, and unit 4 has you write a criterion about exactly that.

    Add fields if you need them.
    """
    return {
        "query": query,              # what the user typed
        "parsed": {},                # description / size / max_price you pulled out of it
        "search_results": [],        # everything search_listings returned
        "selected_item": None,       # the one you chose — goes into suggest_outfit
        "wardrobe": wardrobe,        # the user's wardrobe
        "outfit_suggestion": None,   # what suggest_outfit returned
        "fit_card": None,            # what create_fit_card returned
        "error": None,               # set when the run ended early
    }

def parse(query):
    text = query if query else ""
    max_price = None
    size = None

    words = text.split()
    description_words = []
    i = 0

    while i < len(words):
        word = words[i]

        if word.startswith("$"):
            price_text = word[1:]

            try:
                max_price = float(price_text)
                i += 1
                continue
            except ValueError:
                pass
        
        if word.lower() in ("under", "below", "less"):
            if i + 1 < len(words):
                next_word = words[i + 1]

                if next_word.startswith("$"):
                    try:
                        max_price = float(next_word[1:])
                        i += 2
                        continue
                    except ValueError:
                        pass

        if word.lower() == "size" and i + 1 < len(words):
            size = words[i + 1].strip(" ,").upper()
            i += 2
            continue

        description_words.append(word)
        i += 1

    description = " ".join(description_words).strip(" ,")

    return {
        "description": description,
        "size": size,
        "max_price": max_price,
    }

def listing_search(parsed):
    try:
        import mcp_client

        results = mcp_client.call_tool("search_listings", 
            {
                "description": parsed["description"],
                "size": parsed["size"],
                "max_price": parsed["max_price"]
            })

        return results or []
    except Exception:
        return search_listings(parsed["description"], parsed["size"], parsed["max_price"])

# ── planning loop ─────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """
    Run the loop once and return the finished session.

    Args:
        query:    what the user asked for, in plain language
                  (e.g. "vintage graphic tee under $30, size M").
        wardrobe: a wardrobe dict — get_example_wardrobe() or
                  get_empty_wardrobe() from utils/data_loader.py.

    Returns:
        The session dict. **Check session["error"] first** — if it isn't None,
        the run ended early and the later fields will still be None.

    ─────────────────────────────────────────────────────────────────────────
    TODO — build this, following the branch rule you wrote in Milestone 2.

      1. Start a session with new_session().

      2. Count the times round the loop, and call trace.check_iterations(count)
         on each one before you go again. It raises when the count passes
         MAX_ITERATIONS in config.py — see trace.py.

      3. Parse the query into a description, a size, and a max_price. Regex,
         string splitting, or asking the model are all fine — say which you
         chose in your README. Put the result in session["parsed"].

      4. Call search_listings() with what you parsed.
         Put the results in session["search_results"].

         ⚠️ THIS IS THE BRANCH. If nothing came back:
              - put a message in session["error"] saying what the user could
                change — "No results" is not that message
              - return the session
              - do NOT call suggest_outfit with nothing

      5. Choose an item — the first result is fine. Put it in
         session["selected_item"].

      6. Call suggest_outfit() with the selected item and the wardrobe.
         Put the result in session["outfit_suggestion"].

      7. Call create_fit_card() with the outfit and the item.
         Put the result in session["fit_card"].

      8. Return the session.

    ─────────────────────────────────────────────────────────────────────────
    IN UNIT 4 you come back and add two things:

      • Trace calls. One per step. `trace.step("search_listings", inputs=...,
        returned=...)` — see trace.py. Your README needs the output.

      • A handler for ModelUnavailable, so a bad key produces a message rather
        than a stack trace. The import is already at the top of this file.
    """
    session = new_session(query, wardrobe)
    iterations = 0

    iterations += 1
    trace.check_iterations(iterations)
    parsed = parse(query)
    session["parsed"] = parsed
    trace.step("parse_query", inputs=query, returned=parsed)

    iterations += 1
    trace.check_iterations(iterations)
    matches = listing_search(parsed)
    session["search_results"] = matches
    trace.step("search_listings (MCP)", inputs=parsed, returned=matches)

    if not matches:
        output = (
            f"Your query did not result any results."
            f"Try using broader words. For example, 'jeans' returns more than 'straight petite denim'"
            f"{'' if not parsed['size'] else "Remove the size from the query or try a different one."}"
            f"{'' if not parsed['max_price'] else "Raising your max price may help"}"
        )

        session["error"] = output
        return session

    iterations += 1
    trace.check_iterations(iterations)
    session["selected_item"] = matches[0]
    trace.step("select_best_match", returned=session["selected_item"])

    iterations += 1
    trace.check_iterations(iterations)
    session["outfit_suggestion"] = suggest_outfit(session["selected_item"], session["wardrobe"])
    trace.step("suggest_outfit", inputs=session["selected_item"], returned=session["outfit_suggestion"])

    iterations += 1
    trace.check_iterations(iterations)
    session["fit_card"] = create_fit_card(session["outfit_suggestion"], session["selected_item"])
    trace.step("fit_card", inputs=session["selected_item"], returned=session["fit_card"])

    return session

    


# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(f"  fit_card is {session['fit_card']!r} — it should still be None here")
        return

    item = session["selected_item"] or {}
    print(f"  found:    {item.get('title')} — ${item.get('price')} on {item.get('platform')}")
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")
    _show(run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    ))

    print("\n=== A query it can't ===")
    _show(run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    ))

    print(
        "\nThe second one should stop before the fit card. If both paths look "
        "the same,\nthe branch isn't doing anything yet."
    )
