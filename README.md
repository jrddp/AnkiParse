# Commands
## Deck: !d
> Usage: `!d {DECK}[:SUBDECK]`

Sets the deck that any following cards will be added to

## Question: !q
> Usage: `!q[q] {BODY}`

Opens a new card with `{BODY}` as the front side text

If an existing card is opened, it will be finalized

`{BODY}` can be multiple lines, and will finalize upon the next given command.

### Reverse Card Argument: q
Changes behavior to also add the reverse of the created card. Will not affect Cloze cards.

## Answer: !a
> Usage: `!a {BODY}`

Adds `{BODY}` as the back side text of the opened card

## Replace: !r
> Usage: `!r[s] {REP1}///{REP2}...`

Replaces any "___" (3 underscores) with `{REP}` as a Cloze deletion.

If there are multiple "___", multiple replacements can be seperated by "///". By default, one card will be created hiding all replacements.

Having any `!r` perform on an open card will change it to a Cloze card.

### Sequential Argument: `s`
Changes behavior of multiple replacements to create individual cards for each replacement, rather than one card for all replacements

## Tag: !t
> Usage: `!t[t] {TAG1} {TAG2}...`

Add anki tags to your card (Space seperated)

## Finalize: !f
> Usage: `!f`

Finalizes the currently open card

## Repeat: `!!`
> Usage: `!![at]`

Will use the same values for the last `a` or `t` called for the current card.

# Autoformatting
## Markdown Code Blocks
Any markdown-formatted code blocks will automatically be formatted when creating the card, so long as the respective language is included.

## LaTeX
Since Anki has better support for MathJax than LaTeX, using `$MATH$` or `$$MATH$$` will automatically transform into their MathJax formats when a card is created.