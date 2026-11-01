# Quill: Line Rewrites, v2 (archaic, sketchy, but means well)

Status: DRAFT / prep only. Nothing in `live_12d/r.js` or the asset repo has been edited.
Source: `/workspace/sanctuary/live_12d/r.js` (line numbers as of this read).
Voice: `/workspace/sanctuary_art/lore/quill_martsirt.md` (v2). He is soft, precise and faintly amused, and he is hiding something. He is never menacing, and he gives the player the better question.
Grammar (bible rule): use thou/thee/thy/thine. Use thou hast, thou art and thou wilt. He, she and it take -eth (it learneth). Never use I -eth, we -eth or they -eth.

**Duties are unchanged (all numbers kept):**
- Each rite costs 10,000 gold.
- Slay 4 foes, then choose 1 tome of 6.
- The ceiling is 45 readings.
- Some rites lock others out.
- The ring is plain or magic and is priced on its own. Leave and return to reroll the stock. He sells no rares.
- The Boss Stone gives a choice of six rites, and one rises.

**Location fix:** every "southwest corner" becomes **his scriptorium, north of the square** (tower ~(12.25, −25.15) m; see NPC_MARTSIRT_PLAN.md).

---

## A. Static town lines `gc()`, Quill.lines[0..6] (r.js ~29300–29306)

| id | Old | New |
|---|---|---|
| gc.quill[0] | I keep to the southwest corner of the square, off the road. The town I do not walk. | My scriptorium standeth north of the square, the narrow tower with the patched slates. Seek me there. The rest of the town I do not walk. Not by daylight. |
| gc.quill[1] | The shelves scarce keep a rite. I do, at ten thousand gold. The price bendeth not. | The shelves scarce keep a rite. I do, at ten thousand gold, and the price bendeth not. Ask not where I come by them. I would only tell thee something pleasant. |
| gc.quill[2] | Slay four foes and I shall let thee choose one tome from six. I will not choose it for thee. | Slay four foes and I shall lay six tomes before thee. Thou choosest one. I choose nothing for thee. I have chosen for others, and I keep a list. |
| gc.quill[3] | Read a tome and it stayeth. Forty-five readings is the ceiling. | Read a tome and it stayeth with thee. Forty-five readings is the ceiling. I have known men reach for a forty-sixth. Hush. I have known nothing. |
| gc.quill[4] | Some doors slam shut when thou openest another. Choose with care. | Some rites shut a door when thou openest them. Choose with care, friend. A door that closeth quietly is still a door closed. |
| gc.quill[5] | A ring of plain or magic make sitteth with the books. Both change if thou leavest and returnest. Rare I do not sell. | A ring sitteth with the books, of plain or magic make. Leave and return, and both shall have changed. Rare I do not sell. Rare things have owners, and owners come asking. |
| gc.quill[6] | The oldest scripture nameth no fate. Only the burden of a choice, and no promise that it saveth thee. | The oldest scripture nameth no fate, only the burden of a choice, and no promise that it saveth thee. I copied that line myself. Twice. The second time I believed it. |

## B. Bark table `es.Quill[0..2]` (r.js 27093 `var es`, Quill ~27201–27203)

| id | Old | New |
|---|---|---|
| es.Quill[0] | I keep the southwest corner, off the road. The town I do not walk. | North of the square, the tower with the slit window. That is mine. Knock softly. The coffer hath ears. |
| es.Quill[1] | Ten thousand gold a rite. The price bendeth not, not for friend nor grudge. | Ten thousand gold a rite. The price bendeth not, not for friend nor grudge. Friends, I find, are the dearer customers. |
| es.Quill[2] | The oldest scripture nameth no fate. Only the burden of a choice, and no promise that it saveth thee. | The oldest scripture nameth no fate. Only the burden of a choice. I have carried a few. Mind thy step upon the stair. |
| es.Quill[3] **NEW, optional** (23:30 paper walk to the watch-house, plan §Night) | (none) | Thou didst not see me here, and I did not see thee. A fair trade, and the night keepeth the ledger. |

## C. Interaction lines (r.js 14189–14200)

| id | Old | New |
|---|---|---|
| quill_i01 | Choose your own tome. If I choose, I'll choose wrong on purpose. | Choose thine own tome. Should I choose, I would choose wrong a-purpose, and smile the while. Better thine own hand. |
| quill_i02 | Don't read it here. Not with that thing in the coffer listening. | Read it not here. Not with that thing in the coffer listening. Read it out of doors, by day, where the light hath witnesses. |
| quill_i03 | It's warmer today. I'm writing that down, which I realise is exactly what it wants. | It is warmer today. I am writing that down, which I perceive is precisely what it wanteth. Well. We each keep our ledger. |

## D. Talk lines (r.js 14543), conditions unchanged

| id | Cond | Old | New |
|---|---|---|---|
| quill_t01 | none | Ysara brought bread. I ate the bread. Please tell her I ate the bread. | Ysara brought bread. I ate the bread, every crumb, as I swore. Tell her so, an thou passest her garden. Tell her naught of the second loaf. |
| quill_t02 | none | Bram won't come in this room. Sensible. I'd join him if it weren't my room. | Bram will not cross my threshold. A sensible man. Were it not my room, I would stand out yonder with him and count his trees. |
| quill_t03 | night | I've stopped locking the coffer. If I hide it, it learns the room. If I don't, it learns me. Pick one. | I have ceased to lock the coffer. Hide the tome, and it learneth the room. Leave it be, and it learneth me. A lock is a confession, friend. I had rather be learned. |
| quill_t04 | plague1 done | Four. Four, and the leather went from warm to hot. I keep wanting to call it a fever. It isn't. | Four, and the leather went from warm to hot. I would fain call it a fever. It is not, and thou knowest it is not, and we shall both say fever if any asketh. |
| quill_t05 | plague3 done | The script moves when I look away. I've started looking away on purpose, to see if it gets lazy. It doesn't. | The script moveth when I look away. I have taken to looking away a-purpose, to see whether it groweth lazy. It doth not. Neither do I. We are well matched. |
| quill_t06 | boss vessaline | She ordered the register burned. I carried the torch. I've not said that out loud before. Ysmer didn't carry anything. He just left. | She ordered the register burned, and I carried the torch. I have not said so aloud before. Ysmer carried nothing. He only left. Do me the kindness of not deciding which of us to pity. |
| quill_t07 | act ≥3 | Ysmer had good hands. That's the worst thing I can say about him. Steady hands, good paper, and he never once wasted a line. | Ysmer had good hands. That is the worst I can say of him. Steady hands, good paper, and never once a wasted line. I envied the hands. Tell no one. Envy is a debt. |
| quill_t08 | boss ysmer | It's cold. The book. Stone cold. I sat with it all night waiting for it to be warm again. I'm not sure what I wanted. | It is cold. The book. Cold as a step-stone. I sat with it the night through, waiting for it to warm again. I know not what I wanted. Write not that down. |
| quill_t09 | recent death | You died with a book in your pack. I checked it. Still yours. Still blank where your name should be. Fascinating. Sorry. | Thou didst die with a book in thy pack. I looked. Forgive me, I always look. Still thine, still blank where thy name should sit. Fascinating. Forgive me that also. |
| quill_t10 | regard ≥50 | I've started a page for you. Only facts. Where you went, what you killed. Someone should, who isn't the tome. | I have begun a page for thee. Facts only: where thou wentest, what thou slewest. Someone ought to keep it who is not the tome. Where the page sleepeth is mine own affair. |
| quill_t11 | rain | Damp ruins the paper and the tome likes damp. I've moved the coffer twice. It's still damp. | Damp ruineth paper, and the tome loveth damp. Twice I have moved the coffer. Damp still. I begin to think it is not the weather. |
| quill_t12 | nightmare | The tome has a page for you now. Not your name. A space where it goes. It's very neat. | The tome hath a page for thee now. Not thy name. A space where it goeth. Very neat, very patient. I have stood mine inkpot upon it. A small rudeness, but mine. |

## E. Rumours (r.js 14546), truth flags unchanged

| id | Truth | Old | New |
|---|---|---|---|
| quill_r01 | true | That tome came in on the south road wrapped in a fishing net. The carter wouldn't take coin for it. He wanted it gone. | That tome came up the south road wrapped in a fishing net. The carter would take no coin for it. He wanted it gone, and I wanted it near. Only one of us was wise. |
| quill_r02 | hint | Ysmer took the binding knife when he went into the sea. I gave it to him. I thought he'd use it on himself. In a sense he did. | Ysmer took the binding knife when he went into the sea. I gave it him. I thought he would turn it on himself. In a manner of speaking, he did. Thou hadst this not from me. |
| quill_r03 | false | Sable says she can read any rite on her shelf. Sable can read prices. | Sable saith she can read any rite upon her shelf. Sable can read prices. A useful gift. I have it also. I hide it better. |
| quill_r04 | true | Holt brings me paper from Highmarket. The good mills there stopped making it last winter. Something in the Vault drinks the water. | Holt bringeth me paper from Highmarket, more than one poor scribe could need. The good mills there ceased last winter. Something in the Vault drinketh the water. |
| quill_r05 | hint | The Abbess's choir sang for a week after the burning. Nobody was in the loft. | The Abbess's choir sang a week after the burning. None stood in the loft. I listened from the stair. I did not go up. That is the whole of my courage, in one breath. |
| quill_r06 | true | Ilyra's prayers are four hundred years old. I copy them for her. The grammar's perfect. Hers is better. | Ilyra's prayers are four hundred years old. I copy them for her. The grammar is perfect. Hers is better. Tell her not. She would thank me, and I could not bear it. |

## F. Banter (r.js ~14594–14630)

Under the new banter rule (no reply), only `la` plays. Quill's `lb` in ban_09 would go silent unless that pair is flipped.

| id | Field | Old | New |
|---|---|---|---|
| ban_05 (Quill→Ysara) | la | I ate the bread. | I ate the bread. Truly. Every crumb. |
| ban_06 (Quill→Ilyra) | la | Your third prayer has a scribal error. Four hundred years old. | Thy third prayer beareth a scribal error. Four hundred years old, and I have not the heart to mend it. |
| ban_09 (Wolchen→Quill) | lb | I carried her torch. Drink? | And I carried her torch. Drink? I shall pay. Neither of us shall remember who. |

Suggestion: flip ban_09 so Quill speaks first: la = "I carried her torch, and thou madest mine irons. Drink?"

## G. Role-shared `scribe` strings: need a Quill-only branch (`e.name === 'Quill'`); Sable keeps the current text

| Where | Old (shared) | New (Quill only) |
|---|---|---|
| moodLine r.js 86558 | I was reading. Speak. | I was reading. Speak low, and speak. |
| openShelf r.js ~80342 | Tomes are ten thousand gold. The ring is plain or magic, priced on its own. Leave and return for a new set. Rare I do not sell. | Tomes are ten thousand gold. The ring is plain or magic, priced on its own. Leave and return, and the shelf will have thought better of itself. Rare I do not sell. |
| cold bark r.js ~87584 | I am cold, and I am not crossing the square. | I am cold, and I cross not the square. The scriptorium keepeth what warmth I have. |
| Boss Stone option r.js 80047 | Lay the stone on the desk. Six rites. One of them rises. | Lay the stone upon the desk. Six rites. One of them riseth. Watch which. I shall pretend I did not. |

## H. Quests

### firstread: the LIVE text is the override `Zn.side.firstread` (r.js ~14809–14813). Base `Qi` (~23908) is dead while the override exists.

| Field | Old (live override) | New |
|---|---|---|
| offer | Kill four on the south road of Briarwood. Shamblers, mostly. Then pick one tome of the six. Just one. I'm not made of rites. | Slay four upon the south road of Briarwood. Shamblers, mostly. They will not be missed, not even by themselves. Then choose one tome of the six. One only. I am not made of rites, whatever Holt telleth thee. |
| progress (log) | Four on the south road, then back to Quill in Martsirt. Easy blood, as these things go. | Four on the south road, then back to Quill at his scriptorium, north of Martsirt square. Easy blood, as these things go. |
| doneText | Four down. Pick your rite. The rest stay on the shelf at full price. | Four lie still. Choose thy rite. The rest stay upon the shelf at full price. Friendship I give freely. Books I do not. |
| after | That one's yours. Read it from your pack. The others are still ten thousand, and I'm still not sorry. | That one is thine. Read it from thy pack. The others are ten thousand still, and I am still not sorry. A little sorry. Not enough to lower the price. |

Base Qi firstread (offer, progress, doneText, after) is already archaic. Either delete the override or keep the base text in sync with the above.

### plea, Quill turn-in (LIVE override r.js ~14834)

| Field | Old | New |
|---|---|---|
| after | The great doors stay shut until somebody on the street side remembers they're there. Not today. Today you've a road to walk. | The great doors stay shut until someone on the street side remembereth they are there. Not today. Today thou hast a road to walk, and I a letter to lose somewhere safe. |
| doneText | (third-person narration) | Unchanged. |

### Story chain `pn`, Quill's quoted speech only; the narration is unchanged

| id | Old quote | New quote |
|---|---|---|
| plague1 after (11834) | 'If I hide it, it will learn the room.' | 'Hide it, and it learneth the room.' |
| plague3 offer (11861 base) | 'It names the coast… The drowned are practicing the letters. Put four of them back in the sand before they learn to speak the whole word. There is a book in this for you. Not mine. One the plague has not edited.' | 'It nameth the coast,' he says. 'The drowned are practising the letters. Put four of them back in the sand ere they learn the whole word. There is a book in this for thee. Not mine. One the plague hath not edited.' |
| plague3 offer (14754, Xn override, LIVE?) | '…There's a book in it for you. Not this one. One the plague hasn't touched.' | Use the same new quote as the line above. |
| plague3 doneText (11863) | 'Learn it away from the tome. I do not want them in the same room.' | 'Learn it far from the tome. I would not have them share a room. They would compare notes.' |
| plague3 after (11864) | 'Wynn has been sweeping around the salt statues and pretending that is piety. She has seen the grammar in the faces. Go to the wreck. Do not make her read this.' | 'Wynn hath been sweeping round the salt statues and calling it piety. She hath seen the grammar in the faces. Go to the wreck. Spare her the reading of this.' |

Check: the `Xn` story overrides appear to merge only where wired. Per the earlier read, only Qi side quests apply overrides (r.js 24407). Confirm whether Xn.plague3 actually renders before choosing which line to edit.

## I. Location and UI text (not his voice; fix the location)

| Where | Old | New |
|---|---|---|
| r.js 79013 (town enter) | …Quill waits in the southwest corner. | …Quill keeps his scriptorium, north of the square. |
| r.js 81830 (return from chapter) | Martsirt. Your legs are yours again. Quill waits in the southwest corner. The south gate is the Ashen Coast. | Martsirt. Your legs are yours again. Quill keeps his scriptorium, north of the square. The south gate is the Ashen Coast. |
| r.js 88540 (rite bar hint) | No rite yet. Tomes are rare. Quill wanders Martsirt. | No rite yet. Tomes are rare. Quill keeps them, north of Martsirt square. |
| r.js 92870 (rites panel) | No rites yet. Tomes are rare. Quill wanders Martsirt. | No rites yet. Tomes are rare. Quill keeps them, north of Martsirt square. |

## J. Not touched / for owners

- `sanctuary_art/lore/quill_martsirt.md` still says "southwest corner" (Where), and voices.json (if present) still tags Quill as anxious/modern. The art/lore owner should update both. I did not edit them.
- Boss epitaphs (`warmbinding`, etc., ~14736) are not attributed to Quill, so they are left alone.
- Backstory: the game lines (he was Vessaline's torch-bearer, he gave Ysmer the knife) are kept as-is. Lore v2 hints are only voice. Flag any conflict with Brian.
- The firstread/plea `progress` fields and narration are kept third-person on purpose.
