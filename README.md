# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

FitFindr is a tool for users to find clothes among a series of 40 second-hand listings and
determine how the best match for their query fits in with the rest of their wardrobe. It also
writes a caption describing your new find. To use it, users can use following command in their 
CLI: `python app.ask 'query'` where queries are of the format "90s track jacket in size M" or
"denim jacket under $50". For empty matches, it suggests three changes, words, size, and max
price, to ensure you can adapt your queries.

---

## Tool Inventory

### `search_listings`

- **What it does:**
     Searches the listings for items matching a given description and returns matches, with the best match being first.
- **Inputs:** 
     - description (str): Keywords describing the user's query
     - size (str | None): The size of the garment the user is searching for. Can be None to skip filtering by size
     - max_price (float | None): The ceiling price the user is willing to pay. Can be None to skip filtering by price
- **Returns:**
     A list of matching listing dictionary objects, each with `id`, `title`, `description`, `category`, `style_tags`, `size`,
     `condition`, `price`, `colors`, `brand`, and `platform`. Sorted with the best match first.
- **When it has nothing:**
     Returns an empty list.

### `suggest_outfit`

- **What it does:**
     Suggests two outfits the user can wear based on a given thrifted item and the user's wardrobe.
- **Inputs:**
     - new_item (dict): A listing dictionary of the thrifted item the user wants to use
     - wardrobe (dict): A wardrobe dictionary where the key `items` is a list of item dictionaries.
- **Returns:**
     A non-empty string with outfit suggestions or general styling advice to go with the thrifted item.
- **When it has nothing:**
     If given an empty wardrobe, the funciton returns a non-empty string that give general styling advice.
     It never returns an empty string, an exception, or None.

### `create_fit_card`

- **What it does:**
     Writes a short caption that someone would post about their thrift find and the outfits that go with it.
- **Inputs:**
     - outfit (str): An outfit suggestion (obtained from `suggest_outfit`)
     - new_item (dict): The listing dictionary for the new thrifted outfit
- **Returns:**
     A non-empty string that reads like the caption to a post about the thrifted item. The string should
     mention the item, its price, and its platform once, along with its vibe.
- **When it has nothing:**
     If the `outfit` string is empty, it returns a description about the item and its vibe.

---

## Planning Loop

**Branch rule:**
If `search_listing` returns an empty list, a message is returned to the user naming the things they could change, including the description, price, and size. It then returns without calling `suggest_outfit`. Otherwise, it takes the first result in the list and sends it to `suggest_outfit`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** 
The query is parsed by splitting it into words, removing fluff words that don't affect the matching, removing all matches that do not adhere to the price and size filtering, then comparing the query words with the cleaned keywords from each listing.

**What moves through the session:** 
The first match from `search_listings` moves through the session.

---

## Sample Run

**One full query**

```
$ python app.py ask 'college crewneck size XL under $25'

  Found:    Oversized College Crewneck — Faded Red — $21.0 on thredUp

  Outfit:   Outfit 1: Pair the oversized college crewneck with the baggy straight-leg jeans, black crossbody bag, and chunky white sneakers. Add the brown leather belt to define the waist.

Outfit 2: Layer the oversized college crewneck over the white ribbed tank top, paired with the wide-leg khaki trousers and black combat boots.

  Fit card: I seriously manifested this Oversized College Crewneck in faded red the second I saw it sitting on thredUp for just $21. I am living in this exact piece this season, especially thrown over wide-leg khaki trousers with chunky black combat boots and a peek of a ribbed white tank. When I want a more laid-back vibe, I just tuck it into baggy straight-leg jeans with a leather belt and my favorite white sneakers. It has that perfectly broken-in athletic vintage feel that usually takes years to find.

```

$ python app.py ask 'lace blouse size S under $15'

Your query did not result any results.Try using broader words. For example, 'jeans' returns more than 'straight petite denim' Remove the size from the query or try a different one. Raising your max price may help.

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

[{'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description':'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None,'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'],'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100 cotton, soft and worn-in.', 'category':'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'],'brand': None, 'platform': 'depop'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}]

$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=0))"
[]

```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
Outfit 1:
Vintage Levi's 501 Jeans — Medium Wash
White ribbed tank top
Black cropped zip hoodie
Chunky white sneakers
Black crossbody bag

Outfit 2:
Vintage Levi's 501 Jeans — Medium Wash
Oversized grey crewneck sweatshirt
Vintage black denim jacket
Black combat boots
Brown leather belt


```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Scored these vintage Levi's 501 Jeans — Medium Wash for just $38 on depop and honestly, they fit like an absolute dream. I’m keeping it super simple and throwing them on with my favorite beat-up white sneakers for running errands today. Nothing beats that broken-in denim feel right out of the box.


---

## How I Used AI

**Moment 1**

- *What I asked for:* I asked Claude to explain how an agent loop and help me go step by step through the follow-along code.
- *What came back:* It told me what I should set up and what my final output should look like.
- *What I changed:* It didn't mention how I should test my loop so I added some more cases.

**Moment 2**

- *What I asked for:* I asked ChatGPT to help me write up a parsing function for my query.
- *What came back:* It returned code that went word by word through the query and returned the necessary information as a dict.
- *What I changed:* It forgot the unpack the dictionary when sending my results to the next step so I added that.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching run completes all 3 tools | 4/5 | PASS | PASS | PASS | PASS | PASS | MET |
| 2. Impossible query stops before second tool | 5/5 | PASS | PASS | PASS | PASS | PASS | MET |
| 3. Item in session passes through three tools | 5/5 | PASS | PASS | PASS | PASS | PASS | MET |
| 4. Fit card contains title and price | 5/5 | PASS | PASS | PASS | PASS | PASS | MET |
| 5. Caption includes natural sessions | 4/5 | PASS | PASS | PASS | PASS | PASS | MET |

**Real output from one try**, pasted as text, naming the file and function
that produced it:


**Criterion 1**

From `agent.py::run_agent` via the log:

- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Outfit suggestion:

```
Outfit 1:
Y2K Baby Tee — Butterfly Print
Baggy straight-leg jeans, dark wash
Chunky white sneakers
Black crossbody bag

Outfit 2:
Y2K Baby Tee — Butterfly Print
Wide-leg khaki trousers
Black combat boots
Brown leather belt
```

Fit card:

```
I couldn't believe my luck finding this Y2K Baby Tee — Butterfly Print while digging through the racks yesterday. I grabbed it for just $18 on depop and knew it would be my new favorite piece. Today I'm styling it with dark baggy denim and chunky sneakers, but tomorrow I'll swap those for khaki trousers and combat boots.
```

**Criterion 2** 
From `agent.py::run_agent` from the log:

```
- stopped early: yes — Your query did not result any results.Try using broader words. For example, 'jeans' returns more than 'straight petite denim'Remove the size from the query or try a different one.Raising your max price may help
- selected_item: (none)
- search_results: 0
```

**Criterion 3**
From the trace lines produced by `trace.py::step `
```
[1] parse_query
      in:  tan bag under $40
      out: dict with keys: description, size, max_price
[2] search_listings (MCP)
      in:  dict with keys: description, size, max_price
      out: 6 items: Mini Shoulder Bag — Tan Leather, Bucket Hat — Reversible, Brown Plaid, Vintage Knit Vest — Argyle Brown/Cream … +3 more
[3] select_best_match
      out: Mini Shoulder Bag — Tan Leather ($38.0, poshmark)
[4] suggest_outfit
      in:  Mini Shoulder Bag — Tan Leather ($38.0, poshmark)
      out: Outfit 1: White ribbed tank top Wide-leg khaki trousers Black combat boots Mini Shoulder Bag — Tan Leather  Ou…
[5] fit_card
      in:  Mini Shoulder Bag — Tan Leather ($38.0, poshmark)
      out: I can’t believe I scored this gorgeous Mini Shoulder Bag — Tan Leather for only $38 on poshmark. It instantly …
```

**Criterion 4**
All five cards have the same title and price, from `tools.py::create_fit_card`:

```
Found this dreamy Mini Shoulder Bag — Tan Leather on poshmark for only $38 and she is officially my new everyday go-to. I love throwing it over an oversized grey crewneck and baggy jeans for running errands, or dressing it up with khaki trousers and combat boots. It’s the ultimate little vintage piece that somehow ties every single outfit together.
```

**Criterion 5**
All card captions are made of natural sentences, from `tools.py::create_fit_card`:

```
Just scored the ultimate Knit Cardigan — Chunky Brown for only $35 on depop and I am already obsessed. I threw it on today over a crisp white ribbed tank, dark wash baggy jeans, and my trusty chunky white sneakers for the coziest coffee run. Later this week, I'm definitely pairing it with wide-leg khaki trousers, a cropped black hoodie, and combat boots for that perfect messy-chic vibe.
```

## Verdicts and Diagnoses

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Matching run completes all 3 tools | MET (5/5) | The target was 4/5. Every query with a match successfully went through all three tools. |
| 2 | Impossible query stops before second tool | MET (5/5) | All impossible queries stopped before the second tool 5 out of 5 times. |
| 3 | Item in session passes through three tools | MET (5/5) | Following the trace shows that each item query passes through all three tools 5 out of 5 times. |
| 4 | Fit card contains title and price | MET (5/5) | Every fit card included the title from the listing and its price in the form `$,<price>` |
| 5 | Caption includes natural sessions | MET (5/5) | Every fit card's caption was in natural sentences, without bullet points or syntax. |


**Diagnoses**

Some of the captions, while containing the title of the listing, did not properly capitialize it. This makes it difficult to distinguish the listing from the rest of the caption. To fix this, I tweaked the prompt to change this. 

---

## Loop Trace


**Happy path**

```
[1] parse_query
      in:  vintage low-rise jeans under $30
      out: dict with keys: description, size, max_price
[2] search_listings (MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Low-Rise Cargo Pants — Khaki, Straight Leg Black Jeans — Faded, Leather Belt — Brown, Braided … +7 more
[3] select_best_match
      out: Low-Rise Cargo Pants — Khaki ($27.0, poshmark)
[4] suggest_outfit
      in:  Low-Rise Cargo Pants — Khaki ($27.0, poshmark)
      out: Outfit 1: Pair the Low-Rise Cargo Pants — Khaki with the White ribbed tank top, the Black cropped zip hoodie, …
[5] fit_card
      in:  Low-Rise Cargo Pants — Khaki ($27.0, poshmark)
      out: I seriously gasped when I scored these vintage Low-Rise Cargo Pants — Khaki for only $27 on poshmark. They are…

  Found:    Low-Rise Cargo Pants — Khaki — $27.0 on poshmark

  Outfit:   Outfit 1: Pair the Low-Rise Cargo Pants — Khaki with the White ribbed tank top, the Black cropped zip hoodie, and the Chunky white sneakers.

Outfit 2: Pair the Low-Rise Cargo Pants — Khaki with the Oversized grey crewneck sweatshirt, the Brown leather belt, and the Black combat boots.

  Fit card: I seriously gasped when I scored these vintage Low-Rise Cargo Pants — Khaki for only $27 on poshmark. They are the ultimate throwback piece for my wardrobe rotation. I am obsessed with styling them either with a cropped hoodie and chunky sneakers for running errands, or throwing on an oversized grey crewneck and combat boots for an effortlessly edgy coffee run.

2 model calls this session, 500 prompt + 141 output tokens
```

**Empty search**

```
[1] parse_query
      in:  vintage low-rise jeans under $0
      out: dict with keys: description, size, max_price
[2] search_listings (MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)

  Your query did not result any results.Try using broader words. For example, 'jeans' returns more than 'straight petite denim'

```

**On the MCP move:** <!-- what changed in your code, and whether anything behaved differently afterwards. If the rewire didn't work, say exactly where it broke — the error text and the last thing that worked. That earns the point in full. -->



---

## The Improvement

**What I changed:**
To improve the diagnoses, I tweaked the prompt and specified that the title of the listing should be capitalized in the same way.

**Which failure it was meant to fix:**
While there were no misses, this tightened the wording to make the listing more obvious in the

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching run completes all 3 tools | 4/5 | PASS | PASS | PASS | PASS | PASS | MET |
| 2. Impossible query stops before second tool | 5/5 | PASS | PASS | PASS | PASS | PASS | MET |
| 3. Item in session passes through three tools | 5/5 | PASS | PASS | PASS | PASS | PASS | MET |
| 4. Fit card contains title and price | 5/5 | PASS | PASS | PASS | PASS | PASS | MET |
| 5. Caption includes natural sessions | 4/5 | PASS | PASS | PASS | PASS | PASS | MET |


**Did it help, and how do I know:**

It both helped and didn't. More of the captions now include the capitalized title for easier distinguishment, but they also include the color included with the titles, which makes the captions seem more unnatural.



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
