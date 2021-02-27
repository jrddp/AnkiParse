# Commands
## Deck: !d
> Usage: `!d[c] {DECK}[::SUBDECK]` \
> OR `!dt {TAG1} {TAG2}...`

Sets the deck that any following cards will be added to

### Create deck argument: c
Ensures that the specified deck is created if it does not already exist.

### File-wide Tag Argument: t
Changes behavior to setting the default tags to be added onto every card defined in the file after the command.
If this is used again later in the file, the original tags will be overridden.

## Question: !q
> Usage: `!q[qtf] {BODY}`

Opens a new card with `{BODY}` as the front side text

If an existing card is opened, it will be finalized

`{BODY}` can be multiple lines, and will finalize upon the next given command.

### Reverse Card Argument: q
Changes behavior to also add the reverse of the created card. Will not affect Cloze cards.

### True or False Arguments: t or f
Will automatically build a card prefaced with "True or False:", and set the front of the card to "True" (for arg t) and "False" (for arg f)

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
## Markdown Bold/Italics
Markdown &ast;&ast;**bold**&ast;&ast; and &ast;*italics*&ast; will be converted to HTML formatting.

Formatting using underscores  (&#95;&#95;**bold**&#95;&#95; and &#95;*italics*&#95;) are not supported.

## Markdown Images
Any valid markdown-formatted image will automatically be uploaded to Anki and attached to the card.

## Markdown Code Blocks
Any markdown-formatted code blocks will automatically be formatted when creating the card, so long as the respective language is included.

## LaTeX
Since Anki has better support for MathJax than LaTeX, using `$MATH$` or `$$MATH$$` will automatically transform into their MathJax formats when a card is created.