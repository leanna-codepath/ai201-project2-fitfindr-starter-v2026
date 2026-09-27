# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
This criteria lists 4 out of 5 tries instead of 5 out of 5 tries because a matching
that goes through all three tool calls must use the model. Because the model has room
for failure, like hitting the rate limit or a failed connection, a target of 4 out of 5
leaves toom for leeway.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
5 out of 5 is a reasonable target because all impossible queries must stop
before calling `suggest_outfit`. The agent cannot branch into `suggest_outfit` when
it recieves an empty list, especially since that function requires at least one listing
dictionary. There are no other paths for an empty matching.

---

## 3. The item the search function found is the same item in the next two tools

Given a query that matches at least one listing, the same item is used in the next
two tools - for 5 out of 5 tries. This can be confirmed by comparing the `id` fields
between the best match in `search_listings` and the `new_item` in `suggest_outfit` and
the title/price of the item mentioned in the fit card produced by `create_fit_card` 


**Why this target:**
I chose a target of 5 out of 5 because the new thrifted item found in the search should
be static between each step in the loop. If it is not, then a mutation has occurred
somewhere in the loop, which is a bug that needs to be fixed.

---

## 4.The fit card contains the title and price of the item

Every fit card contains the title and price of the thrifted item - 5 out of 5 tries
on an item. 

**Why this target:**
The criteria follows from the previous- you cannot match an item based 
on its title and price if it doesn't appear in the card. It was also be difficult for others
to find the item without this important information.

---

## 5. The caption should only include natural sentences
The caption should only include natural sentences, no bullet points, key: value pairings, 
or otherwise syntactical notation - 4 out of 5 test cases.

**Why this target:**
I picked 4 out of 5 instead of 5 out of 5 because this criterion depends on the variability
of the model, which may decide to use more syntactical notation to reduce the word count or
make it easier to read.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
